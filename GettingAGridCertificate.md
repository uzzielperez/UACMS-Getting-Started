It would be nice if each year or new cycle of students come they could have a similar walkthrough and just update this github repo by submitting a Pull Request.

My grid certificate expired and the documentation on the obtaining or renewing a grid certificate makes me feel overwhelmed so I've decided to point to the important parts of the documentation here. The full tutorial is in GitHub. I'll also discuss some fascinating things about the Worldwide Computing Grid and some practical know-hows on how to submit jobs with it (the way I usually do it).

## Petabytes of data and the Grid

The Large Hadron Collider produces data that's comparable to the data produced by Facebook and Google. As someone described it some time ago, every second proton-proton collisions produce data that could fill up a CD every second. And that was some time ago. Now it's probably about more than a CD every second if we were to record every information possible. So, we have to employ triggers and fast filters that makes a decision on which information are worth keeping. The data collected then gets "watered" down because we don't have an infinite amount of memory. So we as physicists sort of have to decide what we are looking for even if at the onset we aren't super sure where to find new physics. Anyway, the point is, we're swimming through an ocean of information that needs lots of computing power and memory.

These videos right here can better explain the LHC computing grid:

 - [Processing LHC Data Video](https://www.youtube.com/watch?v=jDC3-QSiLB4)
 - [Petabytes of data](https://www.youtube.com/watch?v=0mgXNgD3JFU)

## How to Connect to the grid

You can find the [full instructions here](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookStartingGrid#ObtainingCert).

The long and small texts seem daunting. So you can just go straight here to getting the grid certificate from this [page](https://ca.cern.ch/ca/user/MyCertificates.aspx) to get a grid certificate and download it. (But if this is your first time just go through the registration and all. You might need to read through the [full instructions](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookStartingGrid#ObtainingCert). If you're just renewing then just go straight to getting the certificate and follow the rest of the instructions.)

Once you have your certificate downloaded follow the instructions [here](https://ca.cern.ch/ca/Help/?kbid=024010).

For security issues and for when we have to look up some datasets over the [CMS Data Aggregation Service (DAS)](https://cmsweb.cern.ch/das/) page we'll need to setup the certificate in our browser. The recommended browser is [Firefox](https://ca.cern.ch/ca/Help/?kbid=040111
).

### Using your grid certificate
Copy the certificate to the computer where you will run `voms-proxy-init`

```python
scp myCert.p12 username@cmslpc-sl7.fnal.gov:~/.globus
# and/or
scp myCert.p12 username@lxplus.cern.ch:~/.globus
# Log in to the machine through ssh e.g.

ssh -XY username@lxplus.cern.ch
# or
ssh -Y username@cmslpc-sl7.fnal.gov

cd ~/.globus
# Extract the certificate:
openssl pkcs12 -in myCert.p12 -clcerts -nokeys -out $HOME/.globus/usercert.pem
# Extract the encrypted private key:
openssl pkcs12 -in myCert.p12 -nocerts -out $HOME/.globus/userkey.pem
# You must set the mode on your userkey.pem file to read/write only by the owner, otherwise voms-proxy-init will not use it:
chmod 600 $HOME/.globus/userkey.pem
chmod 600 $HOME/.globus/usercert.pem
# Delete myCert.p12
rm myCert.p12

# Try it out:

voms-proxy-init -voms cms -rfc
```

You should get something like this

```python
Enter GRID pass phrase:
Your identity: /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=username/CN=78323/CN=User Name Here
Creating temporary proxy ...................................................................... Done
Contacting  lcg-voms2.cern.ch:15002 [/DC=ch/DC=cern/OU=computers/CN=lcg-voms2.cern.ch] "cms" Done
Creating proxy .................... Done

Your proxy is valid until Wed Sep 16 23:00:40 2020
```

Once you're all set up and you're pretty sure that your code is working well for a smaller subset of the entire dataset, we can start scaling up and submitting some computing jobs over the grid.
