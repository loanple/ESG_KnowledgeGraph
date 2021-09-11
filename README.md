# ESG_KnowledgeGraph

ESG stands for Environmental, Social, and Governance, which has become a popular segment for investors to promote sustainable and socially responsible investment opportunities.

The project identifies & compares events/topics on various companies and entities across different industries, sectors, geographical locations, countries through the ESG verticals by analyzing numerical variables such as sentiment and relevance score to build a Knowledge Graph.
The Knowledge Graph serves as a tool to visually interpret changing trends in the news by categorizing entities, industries, and geographies through a weighted average sentiment using NLP to gauge overall positivity or negativity scores.

## Problem Statement
The Knowledge Graph model can help find solutions to the research questions on how the various data points interconnect to one another. Questions the Knowledge Graph could potentially answer:
- How do different events impact the various entities, and to what extent does it impact (measured by sentiment and relevance scores)?
- Which sectors are affected by various events in the ESG vertical?
- Which events play a bigger role for the various geographic locations?
- Which sectors are impacted the most by a change in which ESG vertical?
- Which kind of events have a major impact on the ESG vertical?

### Application Potential
_(See ESG_KnowledgeGraph_UseCases for further information on usecase)_
#### Asset Management
- Review events and relation between entities that become popular over time to increase or decrease investment.
 
#### Risk Management
- Mitigate the risks of investing in sectors having low ESG scores compared to the sectors having high ESG scores.
- Asset managers / traders can use this information to make strategic portfolio building decisions, such as what to long (e.g. equities associated with positive overall scores) and what to short (e.g. those associated with negative overall scores).
 
##### Engagement and thought leadership
- Identifying management communities in the market concerned about sustainable development goals while obtaining financial gains.


## Dataset 
The dataset offers intricate information regarding open news and blog sources to provide a thorough analysis on events happening today. The derived analytics to quantifies sentiment and relevance of an article to an entity by using NLP algorithms that denote key words. 

## Process
1. **Data Exploration** (See _1_Data Analysis.ipynb_)
2. **Data Manipulation** (See _2_KG_SetUp_DataManipulation.ipynb & 2_KG_Documentation.pdf_ for further information)
In order to set up the data for the Knowledge Graph, nodes need to be manipulated from the dataset while maintaining their connections via edges from the dataset. 
     
     <br>_Node Types_:</br>
     - Event Groups (ESG) that each have various events under them
     - Events (e.g. Air Quality, Business Ethics, Supply Chain, Customer Privacy, etc)
     - Entity refers to an institution or company.
     - Sector refers to an indusry that an entity operates in.
     
    <br>_Node Sizes_ - reflects the extent of discussion associated with the node over the selected observation period. </br>

    <br>_Node Color_ - shows overall average sentiment on a given node (i.e. sector, entity, or event), mapped to a color schema that ranges from extremely negative to extremely positive.</br>

    <br>_Node Shape_ delienated in 5 various shapes representing the different node types.</br>

    <br>_Edge Width_ - the connection between nodes that represent proportional number of documents that are relevant between both.</br>

4. **Knowledge Graph Visualization** (See _3_KG_Interactive_Visualization.py_)
Using the NetworkX package to build the The Knowledge Graph database, where each node represented entities while edges represented the connection between the two in the dataset. The visualization is graphed using Plotly which is then exported to Dash, an open source platform, that loads interactive graphs.











