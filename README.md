# Context
This is a summer 2021 project developed by Julia Cwiek. 

# What is the Problem?
Twitch uses Amazon EC2 in order to host applications running on the AWS infrastructure. However, the vulnerability data that is being collected on these EC2 instances is inconsistent across OS types. Most notably, the data collected on vulnerable applications running on Ubuntu EC2 instances do not contain CVE ids, or any other references to the vulnerabilities themselves, while applications hosted on other OS types (such as Windows, Amazon Linux and Red Hat Linux) contain either a CVE id or KB id. 

This is problematic because Ubuntu instances make up over 10% of the Twitch fleet, and without any reference to the vulnerabilities existing on these Ubuntu instances, we lack the necessary data that would allow users to easily understand their impact, and the resources we would need to make informed decisions on what vulnerabilities to focus on burning down in our Vulnerability Management program.

# How does this Project Solve the Problem?
Given the data collection gap on vulnerable packages installed across Ubuntu EC2 instances (i.e. the lack thereof of a CVE id or any other type of vulnerability identification), we built a pipelined solution (a.k.a this project!) to ensure that vulnerable packages installed on Ubuntu EC2 instances have the required additional contextual information (i.e. CVE id) needed to ensure that we have the same foundational vulnerability data across different OS types. 
