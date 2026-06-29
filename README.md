\## Beam Me Up



Beam Me Up is an interactive Streamlit application for the analysis and visualization of planar beam and frame structures. It is intended for teaching and demonstration purposes in introductory structural mechanics and engineering mechanics courses.



The app allows users to define simple beam and frame systems, assign supports, loads, member-end releases, internal hinges, and cross-section profiles, and then compute and visualize support reactions, displacements, section forces, stresses, mass, and estimated material costs.



\## Purpose



The main purpose of this app is to support the learning of structural mechanics by making the connection between mechanical modeling, boundary conditions, internal forces, and deformation behavior more visible and interactive.



In particular, the app is designed to help students explore questions such as:



\* How should a real structural system be idealized as a beam or frame model?

\* Where are nodes required in the mechanical model?

\* How do supports, hinges, and member-end releases affect the structural behavior?

\* How do normal force, shear force, and bending moment diagrams change under different loading and support conditions?

\* How do profile properties influence stresses, deformations, mass, and cost?



\## Features



The app currently supports:



\* Definition of planar nodes and beam/frame members

\* Support conditions with translational and rotational restraints

\* Nodal forces and nodal moments

\* Uniformly distributed member loads

\* Member-end moment releases

\* Internal hinges

\* Linear-elastic Euler-Bernoulli beam/frame analysis

\* Computation of support reactions

\* Computation of nodal displacements and rotations

\* Visualization of deformed shapes with adjustable graphical scaling

\* Visualization of normal force, shear force, and bending moment diagrams

\* Display of global extrema in section-force diagrams

\* Basic stress estimates based on axial force and bending moment

\* Profile selection including simplified teaching profiles, timber profiles, and selected steel sections

\* Estimation of structural mass and material cost



\## Modeling assumptions



The app is based on a simplified linear-elastic planar beam/frame model. The following assumptions apply:



\* Small deformations

\* Linear-elastic material behavior

\* Plane beam/frame behavior

\* Euler-Bernoulli beam theory

\* No shear deformation

\* No geometric nonlinearity

\* No material nonlinearity

\* No stability analysis

\* No torsion

\* No code-compliant structural design verification



The stress values are simplified estimates based on axial force and bending moment. They are intended for plausibility checks and teaching purposes only.



\## How to use the interface



Define the structural model by entering nodes, members, supports, loads, and optional releases or hinges.



A new node is required whenever a point has mechanical relevance in the model. This is the case in particular when:



\* a member starts or ends at that point,

\* a support is located at that point,

\* a nodal force or nodal moment is applied at that point,

\* the geometry changes direction,

\* several members are connected at that point,

\* a continuous beam has an intermediate support.



For example, a continuous beam from `A` to `C` with an intermediate support at `B` should be entered using the nodes `A`, `B`, and `C`, and the two members `A-B` and `B-C`.



If no moment release is assigned at `B`, the beam remains continuous over the intermediate support. The support at `B` constrains the selected displacement components, but it does not automatically create an internal hinge.



Member-end releases define moment releases at specific member ends. They are useful, for example, for modeling hinged connections. Internal hinges can also be introduced using the internal-hinge table.



\## Local installation



Clone the repository and install the required packages:



pip install -r requirements.txt



Then run the app with:



streamlit run beam\_me\_up.py



Depending on the actual file name in your repository, replace `beam\_me\_up.py` with the corresponding Python file name.



\## Requirements



The app requires Python and the following Python packages:



streamlit

numpy

pandas

plotly



\## License



The source code of this application is released under the MIT License. See the `LICENSE` file for details.



\## AI-assisted development



The concept, user interface structure, and parts of the Python/Streamlit implementation were developed with assistance from OpenAI ChatGPT, GPT-5.5 Thinking, June 2026.



\## Disclaimer



This app is intended for teaching and demonstration purposes only. It is based on a simplified linear-elastic planar beam/frame model and does not replace professional engineering verification, safety assessment, or code-compliant structural design.



No warranty is provided for the correctness, completeness, or suitability of the results for practical engineering applications.



