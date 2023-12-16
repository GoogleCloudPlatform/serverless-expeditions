/*
  Copyright 2023 Google LLC

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/
import express from 'express';
import * as gAuth from 'google-auth-library';

const app = express();
// Validate the IAP header first.
app.use(validateIapHeader);
// If validation succeeds, handle the request. In this case, return static
// files from the "public" directory. But it could be to run code instead:
//
//   app.get('/', (req, res) => {
//     res.send(`Hello ${req.userEmail}!`);
//   })
//
app.use(express.static('public'));

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`API listening on port ${port}`);
});

async function validateIapHeader(req, res, next) {
  try {
    const token = req.header('x-goog-iap-jwt-assertion');
    if (!token) throw 'x-goog-iap-jwt-assertion header not found';
    console.log('x-goog-iap-jwt-assertion:', token);
    const oAuth2Client = new gAuth.OAuth2Client();
    const keys = await oAuth2Client.getIapPublicKeys();
    const audience = '<Audience value from IAP>';
    const ticket = await oAuth2Client.verifySignedJwtWithCertsAsync(
      token,
      keys.pubkeys,
      audience,
      ['https://cloud.google.com/iap']
    );
    // Attach decoded email and id to the request so other code can read them.
    req.userEmail = ticket.payload.email;
    req.userId = ticket.payload.sub;
    // Hand off to the next middleware or handler.
    next();
  }
  catch(ex) {
    // Log the exception so the administrator can see it.
    console.log(ex.toString());
    // An exception probably means that the header wasn't set or that it wasn't
    // signed properly. Stop processing the request and return code 403.
    res.status(403).send('Forbidden');
  }
}
