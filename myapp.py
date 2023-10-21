import cohere
import streamlit as st

co = cohere.Client("LDQRLMWbhOcYF6WLZMmDtCg1QsmTdbPm9siqj8VN")

def generate_idea(topic_input, target_audience, creativity):
    """
    Generate jingle idea given the subject and the audience
    Arguments:
    topic_input(str): the subject name
    target_audience(str): the audience value
    Returns:
    jingle(str): the music idea
    """
    if target_audience == "Kids":
        target_modifier = "for a kid"
    elif target_audience == "High schoolers":
        target_modifier = "for a school test"
    else:
        target_modifier = "for a college test"
        

    topic_prompt = f"""write a jingle that briefly teaches {topic_input} {target_modifier}"""

    # Call the Cohere Generate endpoint
    response = co.generate(
        model="command",
        prompt=topic_prompt,
        max_tokens=1000,
        temperature=creativity*0.02,
        k=8,
    )
    jingle = response.generations[0].text
    
    return jingle


# The front end code starts here

st.title("Song Generator")

form = st.form(key="user_settings")
with form:
    # User input - Topic of study
    topic_input = st.text_input("What you want sutdy today? (topic)", key="topic_input")

    # Create a two-column view
    col1, col2 = st.columns(2)
    with col1:
        # User input - The 'temperature' value representing the level of creativity
        creativity_input = st.slider(
            "Creativity",
            value=5,
            key="creativity_input",
            min_value=0,
            max_value=10,
            help="Lower values generate more “predictable” output, higher values generate more “creative” output",
        )
    with col2:
        # User input - The 'temperature' value representing the level of creativity
        target_audience = st.radio(
            "Target Audience",
            key="target-audience",
            options=["Kids", "High schoolers", "College Students"],
        )
        
    # Submit button to start generating ideas
    generate_button = form.form_submit_button("Generate Idea")

    if generate_button:
        if topic_input == "":
            st.error("Topic field cannot be blank")
        else:
            st.subheader("Music ideas:")

            st.markdown("""---""")
            idea = generate_idea(topic_input, target_audience, creativity_input)
            idea = idea.replace("\n", "\n\n")
            st.write(idea)
