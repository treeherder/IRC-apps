(ns bot
	(:import (java.net SSLSocket)
	         (java.io BufferedReader InputStreamReader PrintWriter)
					 (java.lang String))
	
(def pf {:name "packetfire.org" :port 6667 :nick "suckbot"})
(def offblast {:name "gamma.offblast.org" :port 6667})
	
(defn connect [server]
;a socket connection
	(let  [socket ( SSLSocket. (:name server) (:port server))
	
			  ;use this to write to the terminal
				term ( PrintWriter. ( .sock getOutputStream))
				buff ( BufferedReader. ( .sock getInputStream))
				keep
				; define the connection
				keep_alive (do 
											 (. term pr))
					do (keep_alive))
					
					
	defn 
