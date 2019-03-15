# Developers Guide

## About

As a basic premise this entire document is to be very much considered a WIP. Getting the Pi3
up and going initially took me the better part of a month tinkering about with various settings.
The goal of this document is to provide you, the contributer, a step by step guide that will 
vastly accelerate this process.  This document should be considered fluid and subject to change 
at any moment as I find ways to better explain, and better document that process.  Ultimately  
I should be able to automate this entire process through the use of scripts, but, first steps
first.

## Overview

To be broken up into 2 parts, Hardware and Software Setup.  

### Hardware Setup

This bit should be relatively painless as it just requires the Pi to be setup as a wireless access
point enabling other devices to be connected directly to it.  This will likely be the first thing
I automate with a bash script.

### Software Setup

As it stands currently I'm going with a standard Raspian OS.  The standard repositories however
do not suffice for our needs.  Luckily the folks at debian have an unstable branch that contains more
current versions of software I'm using for this project.  
