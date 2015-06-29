This project contains the code to generate, run and test a Swiss-style[1] tournament results database. It is intended for educational purposes only in fulfillment of the "Project 2: Tournament Results" for the Udacity Full Stack Web Developer Nanodegree program.

# Prerequisites
 - VirtualBox installation (https://www.virtualbox.org/wiki/Downloads)
 - Vagrant installation (https://www.vagrantup.com/downloads)
 - Clone of Vagrant VM for ud197 (git clone http://github.com/udacity/fullstack-nanodegree-vm fullstack)

To run the test suite (exercising all of the Python functions for the tournament database):

From a GitHub shell:
 1. cd fullstack/vagrant
 2. vagrant up (you can turn off the VM with 'vagrant halt')
 3. vagrant ssh (from here you can type 'exit' to log out)
 4. cd /vagrant/tournament
 5. psql -f tournament.sql 
 6. python tournament_results.py

# Credits
Test suite provided by Udacity. tournament database schema (tournament.sql) and Python functions written by Erika Navara.

# References
[1] https://en.wikipedia.org/wiki/Swiss-system_tournament
