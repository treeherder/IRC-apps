(let [sock    (new java.net.Socket "www.google.com" 80)
      ostream (. sock getOutputStream)
      writer  (new java.io.PrintWriter ostream true)
      istream (. sock getInputStream)
      reader  (new java.io.BufferedReader (new java.io.InputStreamReader istream))]
  (do
    (. writer println "GET / HTTP/1.1\r\nHost:www.google.com\r\n\r\n")
    (loop [line (. reader readLine)]
      (if (= nil line)
        nil
        (do
          (println line)
          (recur (. reader readLine)))))
    (. ostream close)
    (. istream close)
    (. sock close))
    (System/exit 0)
