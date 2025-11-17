const tcb = require('@cloudbase/node-sdk');

async function main() {
  const envId = process.env.CB_ENV_ID;
  const secretId = process.env.CB_SECRET_ID;
  const secretKey = process.env.CB_SECRET_KEY;
  if (!envId || !secretId || !secretKey) {
    console.error('Missing CB_ENV_ID / CB_SECRET_ID / CB_SECRET_KEY');
    process.exit(1);
  }

  const app = tcb.init({ env: envId, secretId, secretKey, timeout: 10000 });
  const db = app.database();

  const collections = ['wx_users', 'cms_articles', 'wx_push_tasks'];
  const createResults = {};

  for (const name of collections) {
    try {
      await db.createCollection(name);
      createResults[name] = 'created';
    } catch (e) {
      if (String(e && e.message || '').includes('already exists')) {
        createResults[name] = 'exists';
      } else {
        createResults[name] = 'error:' + e.message;
      }
    }
  }

  const insertPayloads = {
    wx_users: { nickname: 'tester', createdAt: new Date().toISOString() },
    cms_articles: { title: 'Hello CloudBase', content: 'Sample', createdAt: new Date().toISOString() },
    wx_push_tasks: { task: 'demo', status: 'pending', createdAt: new Date().toISOString() }
  };

  const insertResults = {};
  for (const name of collections) {
    try {
      const res = await db.collection(name).add(insertPayloads[name]);
      insertResults[name] = 'inserted:' + res.id;
    } catch (e) {
      insertResults[name] = 'error:' + e.message;
    }
  }

  const readResults = {};
  for (const name of collections) {
    try {
      const res = await db.collection(name).limit(1).get();
      readResults[name] = Array.isArray(res.data) && res.data.length > 0 ? 'readable' : 'empty';
    } catch (e) {
      readResults[name] = 'error:' + e.message;
    }
  }

  console.log(JSON.stringify({ createResults, insertResults, readResults }, null, 2));
}

main().catch((e) => {
  console.error('Fatal:', e);
  process.exit(1);
});