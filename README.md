<div align="center">

<a href="https://github.com/z-serhan/devils-pathway/assets/49225046/6f745092-d85e-4350-b65f-e4f5d568eb65">
  <img src="dplogos.png" alt="dplogo" width="80" height="80">
</a>
  <h3 align="center">Devils Pathway</h3>

  <p align="center">
    A GPT-powered career guidance tool designed for university students to strategize their future career paths.
    <br />
    <br />
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

Our product design aims to foster a harmonious Human-AI collaboration, treating AI as a partner in enhancing students' capabilities while maintaining their control over their career goals. 

Anchored in the **Principled Innovation**, with a focus on **inclusivity** and **reflection**, our product's mission is to enhance human agency in the use of AI tools and to promote the inclusive utilization of AI technologies. 

It does so by offering students three distinct agentic experiences, empowering them to make informed and responsible decisions regarding our system's recommendations. These experiences are deeply rooted in the theory of human agency, which comprises three key concepts: forethought, self-regulation, and self-reflection. Our design thoughtfully integrates these theoretical concepts into the fabric of the product elements.

![Product Design Flowchart](https://github.com/z-serhan/devils-pathway/assets/49225046/f2be9c29-97e5-4790-9b41-df32b3c272c6) Figure 1. Theory-driven product design process

As shown in the graph, the _forethought_ element involves collecting data on student characteristics (e.g., majors, personality types, work values, interests, and skills) to inform career planning. 

The _self-regulation_ element is manifested via leveraging these student profiles to match students with suitable careers and recommend relevant ASU courses and certificates. This process is designed to engage students actively in their learning journey by involving them in plan creation and metacognitive reflection. To enhance student agency, we engaged students in an introspective step with five metacognitive questions. These inquiries encouraged students to reflect on their self-belief, strategies, and behaviors, enabling them to critically assess their confidence, methods to goal attainment, and actions to various scenarios. 

Finally, our career readiness checklist allows students to further evaluate these aspects of their career planning endeavors, offering a practical tool for future _self-reflection_ and goal achievement.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ABOUT THE PROJECT -->
## Design Rationale 

The design incorporates multiple datasets, including career datasets from the O*NET Occupation Database, ASU courses dataset, and ASU minors and certificates dataset.

The [O\*NET Occupation Database](https://www.onetcenter.org/database.html#overview) offers a comprehensive set of variables detailing job characteristics (e.g., job title, descriptions, salary) and worker attributes (e.g., skills, values, personality). Leveraging the O\*NET Database's framework, we selected variables such as major, personality, interests, skills, and work values to guide our career recommendations. However, it's important to note that we didn't directly use these variables from the O\*NET Database. Instead, we employed a combination of GPT with the ONET career dataset (including career names and descriptions), prompting GPT to craft a "_Choose Your Own Adventure_" interactive questionnaire. This approach aims to identify students' personality traits and work values. The narrative and scenarios generated by GPT are tailored based on students' interest inputs, while work values are assessed using the six primary categories from the O\*NET Database: recognition, achievement, working conditions, relationships, independence, and support. This method, combining GPT's flexibility and the O*NET database's structure, ensures our recommendations are both accurate and inspiring.

Considering the plethora of personality assessment instruments available, most of which are questionnaire-based and not suited for our interactive format, we opted for the [RIASEC model](https://personalityjunkie.com/holland-code-riasec-career-interests-myers-briggs-types/). This model outlines six interest traits or domains identified by John Holland and the Strong Interest Inventory, namely Realistic (R), Investigative (I), Artistic (A), Social (S), Enterprising (E), and Conventional (C), collectively referred to as "RIASEC." Based on Holland Occupational Theme theory, RIASEC categorizes individuals into distinct groups. Its widespread application and relevance make it an ideal fit for GPT to generate diverse storylines for our interactive interface. In this setup, students navigate through 8 scenario-based, multiple-choice questions to identify their top 3 RIASEC personality types and work values.

![RIASEC personality](https://github.com/z-serhan/devils-pathway/assets/49225046/d1955dcf-b60e-4ce0-9d2d-218bb190cdca)
Figure 2. RIASEC personality Chart

Taking into account students’ major, RIASEC personality types, work values, personal interests, and skills (prioritizing in that order), the system recommends six potential careers from the O\*NET career datasets, subsequently aligning these recommendations with relevant ASU courses and certificate programs.



<!-- GETTING STARTED -->
## Installation and Setup

This project consists of a frontend application built with Angular and styled using the ASU Library Bootstrap theme, and a backend application powered by Flask in Python. This guide will walk you through setting up both parts.

### Prerequisites
Before starting, ensure you have the following installed:
- [Node.js](https://nodejs.org/)
- [Angular CLI](https://cli.angular.io/)
- [Python 3.8](https://www.python.org/downloads/release/python-380/)

### Backend Setup
#### Setting Up Python Flask
Ensure Python 3.8 is installed on your system.
Create a virtual environment in the backend project directory:

  ```sh
  python3 -m venv venv
  ```

Activate the virtual environment:
On Windows:
  ```sh
 venv\Scripts\activate
```

On Unix or MacOS: 
  ```sh
 source venv/bin/activate
```

Install the required Python packages:
   ```sh
pip install annotated-types==0.6.0 anyio==4.3.0 blinker==1.7.0 certifi==2024.2.2 charset-normalizer==3.3.2 click==8.1.7 distro==1.9.0 exceptiongroup==1.2.0 Flask==3.0.2 Flask-Cors==4.0.0 Flask-SQLAlchemy==3.1.1 greenlet==3.0.3 h11==0.14.0 httpcore==1.0.4 httpx==0.27.0 idna==3.6 importlib_metadata==7.1.0 itsdangerous==2.1.2 Jinja2==3.1.3 MarkupSafe==2.1.5 openai==1.14.2 pydantic==2.6.4 pydantic_core==2.16.3 python-dotenv==1.0.1 requests==2.31.0 sniffio==1.3.1 SQLAlchemy==2.0.29 tqdm==4.66.2 typing_extensions==4.10.0 urllib3==2.2.1 Werkzeug==3.0.1 zipp==3.18.1
```

#### Configurations
Ensure all sensitive tokens and keys are set up correctly. For instance, replace the OpenAI tokens in app.py with your own token to enable API calls.


#### Running Flask
With the virtual environment activated and dependencies installed, you can start the Flask application:

  ```sh
 python app.py
```


### Frontend Setup

#### Installing Angular
First, make sure you have Angular CLI installed. If you haven't installed Angular CLI yet, you can install it globally on your system through npm (Node.js package manager) with the following command:
```bash
npm install -g @angular/cli
```

#### Setting Up ASU Library Bootstrap
Our project utilizes the [ASU Library Bootstrap theme](https://unity.web.asu.edu/@asu/unity-bootstrap-theme/index.html?path=/docs/get-started-get-started--page) for frontend design. To use it, you'll need to obtain a token and install it into your project. Follow the steps below:

Visit the ASU Unity Bootstrap Theme documentation to get started.
Obtain a token for accessing the theme.
Follow the provided instructions to include the theme in your project via npm, using your token.

#### Running the Application
Navigate to the frontend project directory and install the required npm packages:

  ```sh
  npm install
  ```
Then, run the Angular development server:
 
  ```sh
  ng serve
  ```
The application should now be running on http://localhost:4200/.








