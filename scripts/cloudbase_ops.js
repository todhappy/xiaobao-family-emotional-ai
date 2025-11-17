const tcb = require('@cloudbase/node-sdk');

function getApp() {
  const envId = process.env.CB_ENV_ID;
  const secretId = process.env.CB_SECRET_ID;
  const secretKey = process.env.CB_SECRET_KEY;
  return tcb.init({ env: envId, secretId, secretKey, timeout: 10000 });
}

async function main() {
  const action = process.argv[2];
  const payload = JSON.parse(process.argv[3] || '{}');
  const app = getApp();
  const db = app.database();
  try {
    if (action === 'createCollection') {
      const name = payload.name;
      await db.createCollection(name);
      console.log(JSON.stringify({ status: 'created', name }));
    } else if (action === 'insertOne') {
      const collection = payload.collection;
      const doc = payload.doc;
      const res = await db.collection(collection).add(doc);
      console.log(JSON.stringify({ status: 'inserted', id: res.id }));
    } else if (action === 'getOne') {
      const collection = payload.collection;
      const res = await db.collection(collection).limit(1).get();
      console.log(JSON.stringify({ status: 'ok', data: res.data }));
    } else {
      console.log(JSON.stringify({ error: 'unknown action' }));
    }
  } catch (e) {
    console.log(JSON.stringify({ error: String(e.message || e) }));
  }
}

main();