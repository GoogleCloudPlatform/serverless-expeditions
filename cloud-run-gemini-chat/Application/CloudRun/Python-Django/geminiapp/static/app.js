// Toggle the Submit button to a Loading... button, or vice versa
function toggleSubmitButton() {
	const submitButton = document.querySelector('#input-form button[type=submit]');

	// Flip the value true->false or false->true
	submitButton.disabled = !submitButton.disabled;

	// Flip the button's text back to "Waiting..."" or "Submit"
	const submitButtonText = submitButton.querySelector('.submit-button-text');
	if(submitButtonText.innerHTML === 'Waiting...') {
		submitButtonText.innerHTML = 'Submit';
	} else {
		submitButtonText.innerHTML = 'Waiting...';
	}

	// Show or Hide the loading spinner
	const submitButtonSpinner = submitButton.querySelector('.submit-button-spinner')
	submitButtonSpinner.hidden = !submitButtonSpinner.hidden;
}

// Process the user's form input
function processFormInput(form) {
	// Get values from the form
	// TODO: FIX CSRF token
	// const token = form.csrf_token.value.trim();
	const token = ''
	const topic = form.topic.value.trim();
	const model = form.model.value.trim();

	// Update the Submit button to indicate we're done loading
	toggleSubmitButton();

	// Clear the output of any existing content
	document.querySelector('#output').innerHTML = '';

	// Send the question
	send(token, topic, model);
}

// Source:
// https://django.readthedocs.io/en/latest/howto/csrf.html#including-the-csrf-token-in-an-unprotected-view
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function send(token, topic, model) {
	const csrftoken = getCookie('csrftoken');

	fetch("ask", {
		method: "POST",
		headers: {
			'X-CSRFToken': csrftoken,
			'Content-type': "application/json"
		},
		body: JSON.stringify({ token: token, text: topic, model: model })
	})
	.then(response => {
		return response.json();
	})
	.then(data => {
		document.querySelector('#output').innerHTML = data["text"];
		toggleSubmitButton();
	})
	.catch(error => {
		console.log(error)
		toggleSubmitButton();
	})
}

function main() {
	// Wait for the user to submit the form
	document.querySelector('#input-form').onsubmit = function(e) {
		// Stop the form from submitting, we'll handle it in the browser with JS
		e.preventDefault();

		// Process the data in the form, passing the form to the function
		processFormInput(e.target)
	};

	// Update the character count when the user enters any text in the topic textarea
	document.querySelector('#topic').oninput = function(e) {
		// Get the current length
		const length = e.target.value.length;
		// Update the badge text
		document.querySelector('#topic-badge').innerText = `${length} characters`;
	}
}

// Wait for the DOM to be ready before we start
addEventListener('DOMContentLoaded', main);
