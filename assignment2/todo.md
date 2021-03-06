- create two meshes (A & B) using blockMesh
    - schematic of the vertices, blocks, edges
    - figures from paraview to provided mesh details
- obtain steady solution for Re=20 on mesh A
    - 3 contour plots
    - plot of streamlines that shows the detail of the recirculation region
- obtain an unsteady, periodic solution for Re=10 on mesh B
    - 3 contour plots
    - plot that shows time history of 3 nondimensional parameters vs normalized time
- modify meshes based on results from the preliminary solutions
    - modify resolution & domain size
    - create a table for each mesh that provides details including domain sizes & total number of points
    - need blockMeshDict files for each mesh tested
- using the articles from canvas, find the value of the St number for Re=110 for an unconfined circular cylinder
- perform a simulation that reproduces the frequency of the vortex shedding
    - use probes to record data at selected locations
    - use various meshes and time steps
    - write a specific description of the procedure used to obtain the St number
    - create a table of meshes, timesteps, St numbers
- repeat simulations at Re=20 with various meshes
    - plot ur and utheta versus s at three tangential locations
    - create a table of L/D, err, ertheta at the wall for each mesh
    - compare the convergence of velocity components and the two rate of strain components
- extra credit