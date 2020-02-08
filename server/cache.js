export const probeCacheElseFetch = (cache, req, fetch, finalAction) => {
  let key = req.path;
  let cachedValue = cache.get(key);
  if (cachedValue) {
    console.log(`Cache hit with key ${key}`);
    finalAction(cachedValue);
  } else {
    console.log(`Cache miss with key ${key}`);
    fetch().then(fetchedValue => {
      cache.set(key, fetchedValue);
      finalAction(fetchedValue);
    });
  }
};

export const sendCachedJSON = (cache, req, res, onMiss) => {
  probeCacheElseFetch(cache, req, onMiss, (fetchedValue) => {
    res.json({ content: fetchedValue });
  });
};
