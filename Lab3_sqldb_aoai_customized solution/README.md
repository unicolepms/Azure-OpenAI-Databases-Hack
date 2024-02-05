# Overview
This application demonstrates the of Open AI (ChatGPT/GPT-4) to help answer business questions by performing advanced data analytic tasks on a business database.
Examples of questions are:
- Simple: Show me daily revenue trends in 2016  per region
- More difficult: Is that true that top 20% customers generate 80% revenue in 2016?
- Advanced: Forecast monthly revenue for next 12 months starting from June-2018

The application supports Python's built-in SQLITE as well as your own Microsoft SQL Server.
# Quick start with hosted demo application 

1. Enter Open AI and database settings if these were not done during installation (see installation below if you want to install yourself).
    Click on settings. Provide Open AI keys, deployment name and URL for ChatGPT. Optionally, you can provide deployment name for GPT-4 for advanced questions.
    For data, you can use the built-in SQLITE demo dataset or you can choose to specify your own SQL Server. In case you use SQLITE, you don't need to enter details for SQL Server.
    Click on submit to save settings.

2. There are two applications
    - SQL Query Writing Assistant: a simple application that translate business question into SQL query language then execute and display result.
    - Data Analysis Assistant: a more sophisticated application to perform advanced data analytics such as statisical analysis and forecasting. Here we demonstrate the use of [Chain of Thought](https://arxiv.org/abs/2201.11903) and [React](https://arxiv.org/abs/2210.03629) techniques to perform multi-step processing where the next step in the chain also depends on the observation/result from the previous step.
    - Insert Function Assistant: a simple application to persist new data to the database by using natural language (staging table is required which will be explained in the labs)

3. Use SQL Query Writing Assistant        
    - Use a question from the FAQ or enter your own question.
    - You can select ```show code``` and/or ```show prompt``` to show SQL query and the prompt behind the scene.
    - Click on submit to execute and see result.
      
4. Use Data Analyst Assistant      
    - Use a question from the FAQ or enter your own question.
    - You can select ```show code``` and/or ```show prompt``` to show SQL & Python code and  the prompt behind the scene.
    - Click on submit to execute and see result.
    - For advanced questions such as forecasting, you can use GPT-4 as the engine 

# Installation 
The instructions on setting up this application will be included in the labs.
