const markdownit = require('markdown-it');

async function ask_gemini(gemini_api_key, model, question) {
	const host = "https://generativelanguage.googleapis.com";
	const path = "/v1beta/models/gemini-pro:generateContent";
	const url = host + path;

	headers = {
		"x-goog-api-key": gemini_api_key,
		"Content-type": "application/json"
	}

	const data = {
		"contents": [
			{
				"parts":[
					{
						"text": question
					}
				]
			}
		]
	};

	var response = await fetch(url, {
		method: "POST",
		body: JSON.stringify(data),
		headers: headers,
	})
	.then((response) => response.json())
	.then((json) => {
// console.log(JSON.stringify(json));

		if (json["candidates"][0]["finishReason"] == 'SAFETY') {
			console.log(JSON.stringify(json));
			return 'Gemini refused the question for safety reasons';
		}

		return json["candidates"][0]["content"]["parts"][0]["text"]
	});

	const md = markdownit({
		html: true,
		linkify: true,
		typographer: true,
	});

	const html = md.render(response);

	return html;
}

module.exports = {
	ask_gemini: ask_gemini
};
