const bodyparser = require('body-parser');
const urlencodedparser = bodyparser.urlencoded({ extended: false});
const {Firestore} = require('@google-cloud/firestore');
const db = new Firestore();

module.exports = function(app) {

  app.get('/todo', async function(request, response) {
    try {
    const todos_output = await db.collection('todos').get();
    const todos=todos_output.docs.map(doc=>({id: doc.id, item: doc.data().item}));
      response.render("todo", {todos});
    } catch (error) {
      response.status(500).send(error.message);
    }
  });

  app.post('/todo', urlencodedparser, async function(request, response) {
    const data = request.body;
    const newTodo = await db.collection('todos').add(data);
    response.json(newTodo);
  });

  app.delete('/todo/:id', async function(request, response) {
    console.log(`DELETE /todo/${request.params.id}`)
      try {
        const itemDesc = request.params.id.replace('-', ' ');
        const snap = await db.collection('todos').where('item', '==', itemDesc).get();
        if (!snap.empty) {
          for (const doc of snap.docs) {
            await doc.ref.delete();
          };
        }
        response.send('OK');
      } catch (error) {
        console.error(error);
        response.status(500).send(error.message);
      }
  });

}
