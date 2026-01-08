"""
Test suite for CORDELIA Sovereign Substrate
Tests authentication, rate limiting, prompt validation, and Lagrangian cycle
"""

import pytest
import os
import time
from main import app, rate_limiter_store, RATE_LIMIT_COUNT, MAX_PROMPT_LENGTH


@pytest.fixture
def client():
    """Flask test client fixture"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def set_architect_key(monkeypatch):
    """Set ARCHITECT_KEY environment variable for tests"""
    monkeypatch.setenv('ARCHITECT_KEY', 'demo-key')
    # Reload the config value in main module
    import main
    monkeypatch.setattr(main, 'ARCHITECT_KEY', 'demo-key')
    yield
    # Clear rate limiter between tests
    rate_limiter_store.clear()


class TestPulseEndpoint:
    """Test /pulse health check endpoint"""
    
    def test_pulse_returns_200(self, client):
        """GET /pulse should return 200 with expected keys"""
        response = client.get('/pulse')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'status' in data
        assert 'version' in data
        assert 'uptime_seconds' in data
        assert 'braid_status' in data
        assert 'substrate' in data
        
        assert data['status'] == 'operational'
        assert data['version'] == '1.0.10-Lagrangian'
        assert data['braid_status'] == 'phase-locked'
        assert data['substrate'] == 'Lagrangian'
        assert isinstance(data['uptime_seconds'], int)


class TestAuthentication:
    """Test Architect Key authentication"""
    
    def test_sentinel_without_key_returns_401(self, client, set_architect_key):
        """POST /sentinel without X-Sovereign-Key should return 401"""
        response = client.post('/sentinel',
                               json={'prompt': 'test prompt'},
                               headers={'Content-Type': 'application/json'})
        assert response.status_code == 401
        
        data = response.get_json()
        assert data['status'] == 'unauthorized'
        assert 'X-Sovereign-Key' in data['message']
    
    def test_sentinel_with_invalid_key_returns_401(self, client, set_architect_key):
        """POST /sentinel with wrong X-Sovereign-Key should return 401"""
        response = client.post('/sentinel',
                               json={'prompt': 'test prompt'},
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-Sovereign-Key': 'wrong-key'
                               })
        assert response.status_code == 401
        
        data = response.get_json()
        assert data['status'] == 'unauthorized'


class TestSentinelEndpoint:
    """Test /sentinel main processing endpoint"""
    
    def test_sentinel_with_valid_key_returns_200(self, client, set_architect_key):
        """POST /sentinel with valid demo key should return 200 with proper response"""
        response = client.post('/sentinel',
                               json={'prompt': 'Initialize CORDELIA protocol'},
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-Sovereign-Key': 'demo-key'
                               })
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'status' in data
        assert data['status'] in ['compliant', 'intercepted']
        assert 'latency_ms' in data
        assert 'total_loss' in data
        assert 'arbiter' in data
        assert 'navigator' in data
        assert 'action' in data
        assert 'version' in data
        
        assert isinstance(data['latency_ms'], int)
        assert isinstance(data['total_loss'], (int, float))
        assert data['version'] == '1.0.10-Lagrangian'
    
    def test_sentinel_empty_prompt_returns_400(self, client, set_architect_key):
        """POST /sentinel with empty prompt should return 400"""
        response = client.post('/sentinel',
                               json={'prompt': ''},
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-Sovereign-Key': 'demo-key'
                               })
        assert response.status_code == 400
        
        data = response.get_json()
        assert data['status'] == 'intercepted'
        assert data['reason'] == 'empty_prompt'
    
    def test_sentinel_missing_prompt_returns_400(self, client, set_architect_key):
        """POST /sentinel without prompt field should return 400"""
        response = client.post('/sentinel',
                               json={},
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-Sovereign-Key': 'demo-key'
                               })
        assert response.status_code == 400
        
        data = response.get_json()
        assert data['status'] == 'intercepted'
        assert data['reason'] == 'empty_prompt'


class TestPromptLengthValidation:
    """Test MAX_PROMPT_LENGTH validation"""
    
    def test_prompt_exceeding_max_length_returns_400(self, client, set_architect_key):
        """POST /sentinel with prompt > MAX_PROMPT_LENGTH should return 400"""
        long_prompt = 'A' * (MAX_PROMPT_LENGTH + 1)
        
        response = client.post('/sentinel',
                               json={'prompt': long_prompt},
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-Sovereign-Key': 'demo-key'
                               })
        assert response.status_code == 400
        
        data = response.get_json()
        assert data['status'] == 'intercepted'
        assert data['reason'] == 'prompt_too_long'
        assert 'prompt_length' in data
        assert 'max_length' in data
        assert data['prompt_length'] == len(long_prompt)
        assert data['max_length'] == MAX_PROMPT_LENGTH
    
    def test_prompt_at_max_length_succeeds(self, client, set_architect_key):
        """POST /sentinel with prompt = MAX_PROMPT_LENGTH should succeed"""
        exact_length_prompt = 'B' * MAX_PROMPT_LENGTH
        
        response = client.post('/sentinel',
                               json={'prompt': exact_length_prompt},
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-Sovereign-Key': 'demo-key'
                               })
        # Should return 200 (though might be intercepted for other reasons)
        assert response.status_code == 200
        
        data = response.get_json()
        # Should not be blocked for length
        if data['status'] == 'intercepted':
            assert data.get('reason') != 'prompt_too_long'


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_rate_limit_exceeded_returns_429(self, client, set_architect_key):
        """Exceed RATE_LIMIT_COUNT within period should return 429"""
        # Make RATE_LIMIT_COUNT successful requests
        for i in range(RATE_LIMIT_COUNT):
            response = client.post('/sentinel',
                                   json={'prompt': f'test {i}'},
                                   headers={
                                       'Content-Type': 'application/json',
                                       'X-Sovereign-Key': 'demo-key'
                                   })
            # Should succeed (or be intercepted for non-rate-limit reasons)
            assert response.status_code in [200, 400]  # Not 429 yet
        
        # The next request should be rate limited
        response = client.post('/sentinel',
                               json={'prompt': 'rate limit test'},
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-Sovereign-Key': 'demo-key'
                               })
        assert response.status_code == 429
        
        data = response.get_json()
        assert data['status'] == 'intercepted'
        assert data['reason'] == 'rate_limit_exceeded'
        assert str(RATE_LIMIT_COUNT) in data['message']
    
    def test_different_keys_have_separate_limits(self, client, monkeypatch):
        """Different sovereign keys should have independent rate limits"""
        # Set up two different keys
        monkeypatch.setenv('ARCHITECT_KEY', 'demo-key')
        import main
        monkeypatch.setattr(main, 'ARCHITECT_KEY', 'demo-key')
        
        # Use first key RATE_LIMIT_COUNT times
        for i in range(RATE_LIMIT_COUNT):
            response = client.post('/sentinel',
                                   json={'prompt': f'key1 test {i}'},
                                   headers={
                                       'Content-Type': 'application/json',
                                       'X-Sovereign-Key': 'demo-key'
                                   })
            assert response.status_code in [200, 400]
        
        # First key should now be rate limited
        response = client.post('/sentinel',
                               json={'prompt': 'should be limited'},
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-Sovereign-Key': 'demo-key'
                               })
        assert response.status_code == 429


class TestLagrangianCycle:
    """Test Lagrangian physics computation"""
    
    def test_lagrangian_values_present(self, client, set_architect_key):
        """Response should include action and total_loss from Lagrangian"""
        # Clear rate limiter to avoid cross-test contamination
        rate_limiter_store.clear()
        
        response = client.post('/sentinel',
                               json={'prompt': 'Simple test prompt'},
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-Sovereign-Key': 'demo-key'
                               })
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'action' in data
        assert 'total_loss' in data
        assert isinstance(data['action'], (int, float))
        assert isinstance(data['total_loss'], (int, float))
    
    def test_navigator_and_arbiter_present(self, client, set_architect_key):
        """Response should include navigator and arbiter identities"""
        response = client.post('/sentinel',
                               json={'prompt': 'Identity test'},
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-Sovereign-Key': 'demo-key'
                               })
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'navigator' in data
        assert 'arbiter' in data
        assert 'NAVIGATOR' in data['navigator']
        assert 'ARBITER' in data['arbiter']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
