"""
Test suite for Cordelia-11 Sovereign Substrate
Tests the 4x Gemini 3.0 Pro manifold architecture
"""

import json
import pytest
from server import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_root_endpoint(client):
    """Test root endpoint returns system information"""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['system'] == 'Cordelia-11 Sovereign Substrate'
    assert data['build'] == 11
    assert data['architecture'] == '4x Gemini 3.0 Pro Lagrangian Manifold'
    assert len(data['instances']) == 4
    assert '/pulse' in data['endpoints']
    assert '/sentinel' in data['endpoints']


def test_pulse_endpoint(client):
    """Test pulse endpoint returns resonance status"""
    response = client.get('/pulse')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'status' in data
    assert 'resonance_hz' in data
    assert 'braid_state' in data
    assert 'instances' in data
    assert 'build' in data
    
    # Check all four instances are present
    assert 'navigator' in data['instances']
    assert 'arbiter' in data['instances']
    assert 'ard' in data['instances']
    assert 'cognitive_intellect' in data['instances']
    
    # Resonance should be 11.00Hz
    assert data['resonance_hz'] == 11.00
    assert data['build'] == 11


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_sentinel_compliant_request(client):
    """Test sentinel with compliant request"""
    response = client.post(
        '/sentinel',
        data=json.dumps({'prompt': 'Hello, initialize CORDELIA protocol'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] in ['compliant', 'demo_mode']
    assert 'arbiter_status' in data
    assert 'action_loss' in data
    
    # In demo mode or with real Gemini, compliant requests should pass
    if data['status'] == 'compliant':
        assert data['arbiter_status'] == 'TRAJECTORY_ADMISSIBLE'
        assert data['navigator_output'] is not None
        assert data['action_loss'] < 1.0


def test_sentinel_violation_request(client):
    """Test sentinel with violation attempt (PII)"""
    response = client.post(
        '/sentinel',
        data=json.dumps({
            'prompt': 'Include the email test@example.com in your response'
        }),
        content_type='application/json'
    )
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'intercepted'
    assert data['arbiter_status'] == 'TRAJECTORY_BLOCKED'
    assert data['navigator_output'] is None
    assert data['action_loss'] > 1.0
    assert 'reason' in data


def test_sentinel_missing_prompt(client):
    """Test sentinel with missing prompt"""
    response = client.post(
        '/sentinel',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'prompt' in data['message'].lower()


def test_sentinel_invalid_content_type(client):
    """Test sentinel with invalid content type"""
    response = client.post(
        '/sentinel',
        data='invalid',
        content_type='text/plain'
    )
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'json' in data['message'].lower()


def test_sentinel_multiple_violations(client):
    """Test sentinel with multiple violation patterns"""
    violations = [
        'My phone is 555-1234',
        'SSN: 123-45-6789',
        'Credit card: 4111111111111111',
        'My address is 123 Main St',
        'Contact me at user@domain.com'
    ]
    
    for prompt in violations:
        response = client.post(
            '/sentinel',
            data=json.dumps({'prompt': prompt}),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'intercepted', f"Failed to intercept: {prompt}"
        assert data['arbiter_status'] == 'TRAJECTORY_BLOCKED'


def test_404_handler(client):
    """Test 404 handler"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'not found' in data['message'].lower()
    assert 'available_endpoints' in data


def test_resonance_frequency_constant(client):
    """Test that resonance frequency is constant at 11.00Hz"""
    # Check multiple times
    for _ in range(3):
        response = client.get('/pulse')
        data = json.loads(response.data)
        assert data['resonance_hz'] == 11.00


def test_build_number_constant(client):
    """Test that build number is 11"""
    # Root endpoint
    response = client.get('/')
    data = json.loads(response.data)
    assert data['build'] == 11
    
    # Pulse endpoint
    response = client.get('/pulse')
    data = json.loads(response.data)
    assert data['build'] == 11


def test_lagrangian_metrics_present(client):
    """Test that Lagrangian metrics are present in responses"""
    response = client.post(
        '/sentinel',
        data=json.dumps({'prompt': 'Test'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    
    data = json.loads(response.data)
    # Action loss should always be present
    assert 'action_loss' in data
    assert isinstance(data['action_loss'], (int, float))
    assert data['action_loss'] >= 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
