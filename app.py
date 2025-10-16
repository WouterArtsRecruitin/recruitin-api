#!/usr/bin/env python3
"""
Recruitin Labour Market Intelligence API
Flask wrapper for processing Jotform submissions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    """API home/docs endpoint"""
    return jsonify({
        'service': 'Recruitin Labour Market Intelligence API',
        'version': '1.0.0',
        'status': 'operational',
        'endpoints': {
            '/health': 'Health check',
            '/webhook/jotform': 'Jotform webhook handler (POST)'
        },
        'documentation': 'https://github.com/recruitin/labour-market-intelligence'
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Recruitin Labour Market Intelligence API',
        'version': '1.0.0'
    })

@app.route('/webhook/jotform', methods=['POST'])
def jotform_webhook():
    """
    Jotform webhook handler
    Processes form submissions from Recruitin intake form
    """
    try:
        logger.info("Received Jotform webhook")
        
        # Get form data
        form_data = request.form.to_dict()
        logger.info(f"Form data keys: {list(form_data.keys())}")
        
        # Parse rawRequest if present
        raw_request = form_data.get('rawRequest')
        if raw_request:
            import json
            try:
                submission = json.loads(raw_request)
                logger.info(f"Parsed submission ID: {submission.get('submissionID')}")
                
                # Extract answers
                answers = submission.get('answers', {})
                
                # Map question IDs to data
                # Update these based on your actual Jotform question IDs
                extracted_data = {
                    'submission_id': submission.get('submissionID'),
                    'submission_date': submission.get('created_at'),
                    'form_id': submission.get('formID'),
                }
                
                # Extract all answers dynamically
                for q_id, q_data in answers.items():
                    answer = q_data.get('answer', q_data.get('text', ''))
                    question_name = q_data.get('name', f'question_{q_id}')
                    extracted_data[question_name] = answer
                
                logger.info(f"Extracted data: {extracted_data}")
                
                # TODO: Process the submission
                # - Download PDFs
                # - Run analysis
                # - Generate report
                # - Send email
                
                return jsonify({
                    'success': True,
                    'submission_id': extracted_data.get('submission_id'),
                    'message': 'Submission received successfully',
                    'data_received': extracted_data
                }), 200
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Invalid JSON in rawRequest'
                }), 400
        else:
            # No rawRequest, just echo form data
            logger.warning("No rawRequest found, returning form data")
            return jsonify({
                'success': True,
                'message': 'Webhook received (no rawRequest)',
                'form_data': form_data
            }), 200
        
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': {
            '/': 'API home',
            '/health': 'Health check',
            '/webhook/jotform': 'Jotform webhook (POST)'
        }
    }), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        'error': 'Internal server error',
        'message': str(e)
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Recruitin API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
