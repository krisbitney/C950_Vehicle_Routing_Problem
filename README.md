# C950_Vehicle_Routing_Problem
Task: Design an algorithm to solve the Vehicle Routing Problem

See "C950 Project Writeup.docx" document for detailed description of algorithms, data structures, and analysis.

#### Problem description:
We are tasked with designing an algorithm to solve the Vehicle Routing Problem, a generalization of the Traveling Salesman Problem in computer science. The problem requires that we find optimal routes for a set of vehicles that will deliver packages to locations. The problem is NP-complete, so an exact solution is impractical. Rather, we are tasked with finding an approximate solution that is practical to implement and meets the needs of our client.

Our version of the Vehicle Routing Problem includes several constraints. There are two vehicles. Vehicles can hold only 16 of the 40 packages we must deliver. Some packages can only be carried by a particular vehicle. Different packages have different time deadlines by which they must be delivered. Some packages are “delayed” and cannot leave the vehicle hub until certain times. We must assume that management can change the delivery deadline for any package at any time. All of these constraints increase the complexity of the problem.

