import {useCallback, useEffect, useState} from 'react';

const useFetch = (path, transform) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(() => {
    (async () => {
      setLoading(true);
      const resp = await fetch(path);
      if (resp.ok) {
        let fetchedData = await resp.json();
        if (typeof transform === 'function') {
          fetchedData = transform(fetchedData);
        }
        setData(fetchedData);
      } else {
        let respBody;
        try {
          respBody = await resp.clone().json();
        } catch {
          respBody = await resp.text();
        }
        console.error('Request failed: ', respBody);
      }
      setLoading(false);
    })();
  }, []);

  useEffect(refresh, []);

  return [data, loading, setData, refresh];
};

export default useFetch;
