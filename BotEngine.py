import aiml, os

kernel = aiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = os.path.abspath("brain.aiml"), commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")

def get_response(user_request):
    bot_response = kernel.respond(user_request)
    return bot_response
    