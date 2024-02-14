import uuid
import boto3

def lambda_handler(event, context):
    
    client = boto3.client("bedrock-agent-runtime")
    
    session_id:str = str(uuid.uuid1())
    agent_id:str = 'IJ4C2ZP79C'
    agent_alias_id:str = 'ASQA8KJSTZ'
    input_text = event['text']
    
    response = client.invoke_agent(
        inputText=input_text,
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        enableTrace=True
        )
    
    print(response)

    event_stream = response['completion']
    for event in event_stream:
        if 'chunk' in event:
            output_text = event['chunk']['bytes'].decode("utf-8")

    for event in event_stream:
        if 'trace' in event:
            debug = event['trace']['trace']
    print(debug)

    return output_text