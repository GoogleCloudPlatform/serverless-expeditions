const {Firestore} = require('@google-cloud/firestore');

// Instantiates a client. If you don't specify credentials,
// the library will look for credentials in the environment.
const firestore = new Firestore();

// Functions Framework function (uses Express)
exports.function = (req, res) => {
  const animalName = req.params.animalName;
  if (!animalName) res.status(401).send('Invalid Animal Name');
  const querySnapshot = await firestore.collection(animalName).get();
  if (!querySnapshot) {
    const sightings = querySnapshot.docs.map(doc => doc.data());
    res.json({status: 'success', data: {sightings: sightings}});
  } else {
    res.status(404).send({
      status: 'failure', data: {message: `'${animalName}' not found`}
    });
  }
};