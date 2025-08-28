// This file handles the logic for the popup, including capturing user input and sending it to the content script or backend for processing.

console.log('Script loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded');
    
    // Log all elements to see what's available
    console.log('All elements with IDs:');
    const allElements = document.querySelectorAll('[id]');
    allElements.forEach(el => {
        console.log(`- ${el.id}: ${el.tagName}`);
    });
    
    // Try to get elements one by one
    const form = document.getElementById('commandForm');
    const input = document.getElementById('commandInput');
    const responseDiv = document.getElementById('response');
    const testBtn = document.getElementById('testConnection');
    const testResult = document.getElementById('testResult');
    
    console.log('Element check:', {
        form: form ? 'found' : 'NOT FOUND',
        input: input ? 'found' : 'NOT FOUND',
        responseDiv: responseDiv ? 'found' : 'NOT FOUND',
        testBtn: testBtn ? 'found' : 'NOT FOUND',
        testResult: testResult ? 'found' : 'NOT FOUND'
    });
    
    if (!form) {
        console.error('Form not found! Available elements:', document.body.innerHTML);
        return;
    }
    
    // Test connection button (simplified)
    if (testBtn) {
        testBtn.addEventListener('click', function() {
            console.log('Test button clicked');
            if (testResult) {
                testResult.innerHTML = 'Testing...';
            }
            
            fetch('http://localhost:8000/test')
                .then(response => response.json())
                .then(data => {
                    console.log('Test result:', data);
                    if (testResult) {
                        testResult.innerHTML = `✓ ${data.message}`;
                    }
                })
                .catch(error => {
                    console.error('Test error:', error);
                    if (testResult) {
                        testResult.innerHTML = `✗ Error: ${error.message}`;
                    }
                });
        });
        console.log('Test button listener added');
    }
    
    // Form submission (simplified)
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Form submitted');
            
            const command = input ? input.value.trim() : '';
            console.log('Command:', command);
            
            if (!command) return;
            
            if (responseDiv) {
                responseDiv.innerHTML = 'Processing...';
            }
            
            fetch('http://localhost:8000/process_command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    command: command,
                    page_context: {}
                })
            })
            .then(response => {
                console.log('Response status:', response.status);
                return response.json();
            })
            .then(result => {
                console.log('Result:', result);
                if (responseDiv) {
                    responseDiv.innerHTML = result.response || result.error || 'No response';
                }
                if (input) {
                    input.value = '';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (responseDiv) {
                    responseDiv.innerHTML = `Error: ${error.message}`;
                }
            });
        });
        console.log('Form listener added');
    }
    
    console.log('Initialization complete');
});