/**
 * 
 * @param {Map} cache the cache to store and probe from
 * @param {*} req the Express request
 * @param {() => Promise} fetch - function that fetches the content to be cached 
 * @param {VoidFunction} finalAction - called with the value from either the cache
 * hit or the fetch on a cache miss
 */
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

/**
 * Probes the cache and sends the fetched value as JSON, otherwise 
 * @param {Map} cache the cache to store and probe from
 * @param {*} req the Express request
 * @param {*} res the Express response
 * @param {() => Promise} onMiss function to fetch the value if not in the cache
 */
export const sendCachedJSON = (cache, req, res, onMiss) => {
  probeCacheElseFetch(cache, req, onMiss, (fetchedValue) => {
    res.json({ content: fetchedValue });
  });
};
