# Network-Classification-Tool

## Summary
This was a **Smart India Hackathon 2017 grand finale project** done at Ahmedabad under "[Indian Space Research Organisation (ISRO)](https://www.isro.gov.in/)". The real time classification of incoming traffic to web servers using deep packet inspection and Machine Learning algorithms. (Python, PHP, JavaScript, Wireshark, C, LibPcap)

Finale round at SIH

The Proposed solution to the problem includes real time classification of the incoming traffic to a web server using deep packet inspection and machine learning strategies. The proposed solution would be built upon an existing open source web server (Apache web server) to add classification functionalities to it. It would provide the functionality for real time visualization of the incoming traffic categories using a web based interface on the local host. We will Implement a machine learning model from K-Means Clustering, Support Vector Machines, Decision Trees or Neural Network based on the analysis of the dataset and best suited model from one of these would be used for the classification of internet traffic. Basically selection from any of these models would be done based on the accuracy of the algorithm on dataset evaluated over the cross validation test set. Whichever model will provide us with a greater accuracy will be chosen for the implementation of our application. Parameters for the dataset will be chosen based on the relevancy of those features in order to provide our machine learning algorithm to learn classifying the traffic coming to our server into one of the four classes:

Normal Web Traffic P2P Traffic VPN Traffic The Onion Router (TOR)Traffic

In order to fetch the relevant parameters, Deep Packet Inspection will be carried out on the packets by acquiring packets through techniques such as mirror port. The acquired packet’s data part will be examined for understanding the type of traffic and appropriate parameters will be passed to classifying algorithm. Also, a novice strategy for classification of encrypted traffic would be developed based on heuristics and learning from header data to determine the parameters. It would try to classify the encrypted data. In case if the heuristic algorithm is unable to detect the parameters, the traffic will be reported as an additional class of encrypted traffic to the dashboard.

## Technology Stack -

The classification tool would be built using Python. Supporting libraries for machine learning models like numpy, scipy, google TensorFlow, scikit-learn will be used in order to obtain efficiency in performance of algorithm. Its integration with the apache web server would be done in the native language of the server ( i.e. C ). The web visualization tool would be built using HTML, CSS and Javascript and its visualization libraries like d3.js and react.js

## Use Cases -

The use cases for the proposed solution include :
Incoming Traffic Analysis in real time using visualization tools. Blocking the traffic of a particular kind which tends to be malicious to so as to make the system secure. Resource allocation/deallocation to a particular kind of traffic based on the volume of that kind of traffic. In case if the law permits, analysis of data being transmitted through a secure channel to check leakage of any secure or classified data.

## Dependencies -

The dependencies for the project would be : Apache Web Server Python Machine Learning Libraries of python
