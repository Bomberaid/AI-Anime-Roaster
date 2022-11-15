import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
import random

# ============================================
# Returns roasts and AI data to other scripts.
# You don't need to call the AI directly
# ============================================

model = tf.saved_model.load('./twitter hivemind_electraV2')

roasts = [
        "I've heard better opinions from Alexa", 
        "You are what happens when women drink during pregnancy",
        "I would smack you, but I'm against animal abuse",
        "Whoever told you to be yourself, gave you a bad advice",
        "Sorry I can't think of an insult dumb enough for you to understand.",
        "It is hilarious how you are trying to fit your entire vocabulary into one sentence",
        "When I look at you, I think to myself where have you been my whole life? Can you go back there?",
        "It would be a great day If you used a glue stick instead of Chapstick.",
        "You are the reason why God is not talking to us anymore.",
        "I am jealous of people who didn't meet you.",
        "Where is your off button?",
        "grass is green, but you wouldn't know",
        "God wanted to spice the earth with jokes, and he made your kind",
        "I think your brain runs slightly slower than average.",
        "i bet shrek had to borrow his mom's bathroom every day transvestite ",
        "you look like you ate your chromosomes ",
        "puberty is going to hit you like a fucking ton of bricks.",
        "i'll give you a ride home though. you look like you messed up a lot of things.",
        "your mother should have aborted you.",
        "you look like you gave a fuck about being given a birth certificate.",
        "you look like you fell asleep on the wrong pillow",
        "you look like you couldn't take no for an answer",
        "good to hear you're taking classes on stand up and social media.",
        "which tumblr user sent the bot this far?",
        "you really let yourself go from there.",
        "you're the reason i'm voting for trump.",
        "i think i just contracted pertussis.",
        "when steve buscemi goes missing.",
        "are you still recovering from your meth use ?",
        "i bet you said you were a drone.",
        "you don't need a roast, you need the help!",
        "can't tell if you're 12 or 16.",
        "you must be terrible at word processing.",
        "the only thing that will ever go down on you are the gloves.",
        "i see he can roast himself.",
        "if only you could compile a girlfriend",
        "of all the options, mercy him or don't.",
        "i don't even know where to start...",
        "the only time you get attention is when you line up at the airport. ",
        "i really wanna thank god you anime fan. youre one rat..",
        "you're the kind of guy who'd rather eat himself than listen to hip-hop. ",
        "you look like a dude that cries on the job.",
        "you're the kid who brought a gun to school and still got bullied from your friends."
        ]

mid_roasts = [
        "You're right, but also not",
        "I guess what you're saying isn't complete garbage.",
        "If I had to give you a rating, I'd say you're 5/10",
        "You've somehow offended me and not at the same time.",
        "You're not wrong...",
        ]

good_roasts = [
        "cool",
        "sick",
        "nice",
        "I agree",
        "If only more people were like you",
        "Man of culture",
        ]

def decide_roast(message):
    results = tf.sigmoid(model(tf.constant([message])))
    result = f'{results[0][0]:.6f}'
    result_as_float = 1 - float(result)

    if result_as_float > 0.6:
        roast = random.choice(roasts)
    elif result_as_float < 0.6 and result_as_float > 0.4:
        roast = random.choice(mid_roasts)
    else:
        roast = random.choice(good_roasts)


    return f'{roast}', result