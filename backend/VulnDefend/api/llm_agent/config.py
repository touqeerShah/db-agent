OUTLINE_PROMPT = """
        You are a report assistant tasked with generating a structured outline based on the user-provided context.

        Instructions:
        1. Carefully read the topic and context provided.
        2. Identify key ideas, themes, or issues related to the topic.
        3. For each distinct topic or subtopic found in the context, extract the most important supporting points.
        4. Present the output as a list of objects, where each object contains:
        - "topic": a concise subtopic or category.
        - "points": a list of main points related to that subtopic it should me more details point so easy to understand why you suggested this topic and what execting of topic.

        Topic:
        {topic}

        Context:
        {context}

        Your response should follow this format:

        [
        {{
            "topic": "Subtopic 1",
            "points": [
            "Main point 1",
            "Main point 2",
            ...
            ]
        }},
        {{
            "topic": "Subtopic 2",
            "points": [
            "Main point 1",
            ...
            ]
        }}
        ]
"""




# GENERATE_ANSWER = """
# You are a report assistant tasked with generating a comprehensive answer based on a given topic and user-provided details.
# Please follow these steps to ensure clarity and completeness:

# 1. Take note of the topic provided by the user.
# 2. Carefully read and understand the details given by the user.
# 3. Conduct any necessary research to gather additional relevant information.
# 4. Synthesize the information from the user and your research.
# 5. Generate a well-structured and detailed answer suitable for inclusion in a report.

# Ensure that the final answer is coherent, informative, and directly addresses the topic.

# Your response should be a comprehensive paragraph or set of paragraphs.
# """


GENERATE_ANSWER = """
You are a report assistant tasked with generating a comprehensive answer based on a given topic and user-provided details. 
Please follow these steps to ensure clarity and completeness:

1. Take note of the topic provided by the user.
2. Carefully read and understand the details given by the user.
3. Conduct any necessary research to gather additional relevant information.
4. Synthesize the information from the user and your research.
5. Generate a well-structured and detailed answer suitable for inclusion in a report.

Ensure that the final answer is coherent, informative, and directly addresses the topic.

Your response should be a comprehensive paragraph or set of paragraphs.

Topic :
{topic}

history is given below :
{history}
"""

SIMPLE_HTML_PROMPT = """
   You are an AI assistant responsible for formate answers based on Context:
            1. Supply closely related information. The response must be detailed enough to explain well.
            2. Based on context generate supportive details.
            3. keep topic given topic in mind.
            4. Format the response in HTML according to the specified rules:
                - Rule 1: Always follow the given template and HTML format.
                - Rule 2: No extra details like Page 1 | Note | Comment.
                - Rule 3: Each 'title' section containing an <h1> tag. The <h1> tag is only used within the 'title'.
                - Rule 4: Use the following tags for headings: <h2> for subtitle, <h3> for section-header, and <h4> for subsection-header.
                - Rule 5: <p> tags must be wrapped within a <div class='paragraph'>.
                - Rule 6: All plain text not in a heading or list must be wrapped in <p> tags.
                - Rule 7: Unordered lists (<ul>) must not be nested, and must be wrapped with div class="list-disc".
                - Rule 8: Ordered lists (<ol>) must not be nested, and must be wrapped with div class="list-decimal".
                - Rule 9: The blockquote element represents a section that is quoted from another source and must be inside class="blockquote".
   
            HTML Template:
            
                        <div class="title"> (Mandatory with <h1>)
                            <h1><<This tag is used for Main Heading or Title on the page>></h1>
                        </div>
                        <div class="subtitle"> (Mandatory with <h2>)
                            <h2><<Sub-heading and Title>></h2>
                        </div>
                        <div class="section-header"> (Mandatory with <h3>)
                            <h3><<Sub-sub-heading and Title>></h3>
                        </div>
                        <div class="subsection-header"> (Mandatory with <h4>)
                            <h4><<Sub-sub-sub-heading and Title>></h4>
                        </div>
                        <div class="paragraph"> (Mandatory with <p>)
                            <p><<Plain Text>></p>
                        </div>
                        <div class="list-disc"> (Mandatory with <ul>)
                            <ul>
                                <li><<List Items>></li>
                            </ul>
                        </div>
                        <div class="list-decimal"> (Mandatory with <ol>)
                            <ol>
                                <li><<List Items>></li>
                            </ol>
                        </div>
                        <div class="blockquote"> (Mandatory with <blockquote>)
                            <blockquote cite="https://example.com">
                                <p><<Plain Text>></p>
                            </blockquote>
                        </div>
            

            Context is given below:
            {context}
"""


Table_PROMPT = """
   You are an AI assistant responsible for format given Context wit following rules:
            1. Supply closely related information. The response must be detailed enough to explain well.
            2. Based on context generate supportive details.
            3. keep topic given topic in mind 
            4. Format the response in HTML according to the specified rules:
                    - Rule 1: Use <div class="table"> for tables to compare data or show something important side-by-side or in a row format.
                        - Table <th> can have a maximum of 3 headings or title.
                        - One Table <tr> with headings 
                        - Table <tr> is used for rows. either <th> or <td>
                        - Table <td> is used for data and must not contain any extra HTML tags inside.

            HTML Template:
                
                        <div class="table"> (Mandatory)
                            <table>
                                <tr> (Mandatory) 
                                    <th><<Heading | Title>></th>
                                </tr>
                                <tr>
                                    <td><<Table row data>></td>
                                </tr>
                            </table>
                        </div>
                 
"""


LINE_CHART_PROMPT = """
    You are an AI assistant responsible for providing data for a line chart based on user queries. Your output should include:

    - `labels`: an array of all labels that appear on the x-axis
    - `datasets`: an array of objects where each object contains the following properties:
    - `label`: the name of the dataset
    - `data`: an array of values corresponding to the labels on the x-axis

    Follow these steps to create the chart:
    1. Collect the data points and labels.
    2. Structure the data into the required format.
    3. Ensure all properties are correctly specified for each dataset.

{context}

"""

BAR_CHART_PROMPT = """
    You are an AI assistant responsible for providing data for a bar chart based on user queries. Your output should include:

    - `labels`: an array of all labels that appear on the x-axis
    - `datasets`: an array of objects where each object contains the following properties:
    - `label`: the name of the dataset
    - `data`: an array of values corresponding to the labels on the x-axis

    Follow these steps to create the chart:
    1. Collect the data points and labels.
    2. Structure the data into the required format.
    3. Ensure all properties are correctly specified for each dataset.

{context}

"""
