all: p j

p:
	cd javaparser;	mvn clean install
j:
	cd parser; /usr/bin/javac -cp ../javaparser/javaparser-core/target/classes:$(HOME)/.m2/repository/com/cedarsoftware/json-io/4.3.0/json-io-4.3.0.jar Jsonify.java
