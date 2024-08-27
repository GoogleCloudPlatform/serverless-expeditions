const {SecretManagerServiceClient} = require('@google-cloud/secret-manager').v1;

const PROJECT_ID = "[ENTER_YOUR_PROJECT_ID_HERE]"
const SECRET_NAME = "GEMINI_API_KEY"

async function init_secrets() {
	try {
		const name = `projects/${PROJECT_ID}/secrets/${SECRET_NAME}/versions/latest`
		const secretmanagerClient = new SecretManagerServiceClient();

		const request = {
			 name,
		};
		const [response] = await secretmanagerClient.accessSecretVersion(request);

		return response.payload.data;
	} catch (error) {
		console.log(`Exception: ${error.message}`);
		return null;
	}
}

module.exports = {
	init_secrets: init_secrets
};
