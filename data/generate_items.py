"""Item set for knowledge_probe_template.ipynb.

Math items are generated from templates tied to Common Core standards, so every answer is
computed. Science items are hand-written against NGSS performance expectations.
Grades 6-8 science follow the California "preferred integrated" course model (NGSS itself
only gives a 6-8 band), so those grade tags are approximate.

Usage: python generate_items.py ../data/items.jsonl
"""
import json
import random
import sys
from fractions import Fraction

SEED = 2026
rng = random.Random(SEED)

items = []


def add(grade, subject, topic, standard, question, correct, wrong, idx):
    # a trailing "a"/"an" before the blank would hint at the answer's first letter
    for art in (" an", " a"):
        if question.endswith(art):
            question = question[: -len(art)] + " a(n)"
    opts = [correct] + list(wrong)
    assert len(set(opts)) == len(opts), (question, opts)
    rng.shuffle(opts)
    items.append({
        "id": f"{subject[:3]}-g{grade}-{standard}-{idx}".replace(".", "_"),
        "grade": grade,
        "subject": subject,
        "topic": topic,
        "standard": standard,
        # one Q/A frame for every item; sentence stems become fill-in-the-blank questions.
        # Science grades differ in how many stems they have, so check results by `format` too.
        "format": "qa" if question.endswith("?") else "fill_blank",
        "context": ("Question: " + (question if question.endswith("?")
                    else f"Fill in the blank: {question.rstrip(':')} ___.") + "\nAnswer:"),
        "options": [" " + o for o in opts],
        "answer": opts.index(correct),
        "source": standard,
    })


def num_distractors(ans, k=3, spread=None, allow_neg=False):
    # Nearby integers, unique, not equal to ans.
    spread = spread or max(3, abs(ans) // 4)
    out = set()
    while len(out) < k:
        d = ans + rng.choice([-1, 1]) * rng.randint(1, spread)
        if d != ans and (allow_neg or d >= 0):
            out.add(d)
    return [str(d) for d in out]


def math_gen(grade, standard, topic, n, make):
    seen = set()
    i = 0
    while i < n:
        q, ans, wrong = make()
        if q in seen:
            continue
        seen.add(q)
        wrong = list(dict.fromkeys(w for w in wrong if w != ans))[:3]
        while len(wrong) < 3:        # top up with nearby integers when templates collide
            wrong = list(dict.fromkeys(wrong + [w for w in num_distractors(int(ans), allow_neg=int(ans) < 0) if w != ans]))[:3]
        add(grade, "math", topic, standard, q, ans, wrong, i)
        i += 1


# ---------------------------------------------------------------- math
def k_add():
    a, b = rng.randint(1, 4), rng.randint(1, 4)
    a = min(a, 5 - b) or 1
    return f"What is {a} plus {b}?", str(a + b), num_distractors(a + b, spread=2)

def k_next():
    n = rng.randint(3, 18)
    return f"What number comes right after {n}?", str(n + 1), [str(n - 1), str(n + 2), str(n + 10)]

def k_greatest():
    nums = rng.sample(range(1, 11), 4)
    return (f"Which number is the greatest: {', '.join(map(str, nums))}?",
            str(max(nums)), [str(x) for x in nums if x != max(nums)])

K_SHAPES = iter([("sides does a triangle", 3), ("sides does a square", 4),
                 ("corners does a rectangle", 4), ("corners does a triangle", 3)])
def k_shape():
    what, ans = next(K_SHAPES)
    return f"How many {what} have?", str(ans), [str(x) for x in [1, 2, 5, 6] if x != ans][:3]

def g1_add():
    a, b = rng.randint(5, 9), rng.randint(4, 9)
    return f"What is {a} plus {b}?", str(a + b), num_distractors(a + b, spread=3)

def g1_sub():
    a = rng.randint(11, 19); b = rng.randint(3, 9)
    return f"What is {a} minus {b}?", str(a - b), num_distractors(a - b, spread=3)

def g1_tens():
    t, o = rng.randint(2, 9), rng.randint(1, 9)
    if t == o:
        o = (o % 9) + 1
    return f"How many tens are in the number {t}{o}?", str(t), list({str(o), f"{t}{o}", str(t + 1)} - {str(t)})[:3]

def g1_add10():
    a = rng.randint(12, 59); b = 10 * rng.randint(1, 3)
    return f"What is {a} plus {b}?", str(a + b), [str(a + b + 1), str(a + b - 10), str(a + b // 10)]

def g2_add():
    oa, ob = rng.randint(3, 9), rng.randint(3, 9)
    while oa + ob < 10:              # force regrouping
        ob = rng.randint(3, 9)
    a, b = 10 * rng.randint(1, 4) + oa, 10 * rng.randint(1, 4) + ob
    return f"What is {a} plus {b}?", str(a + b), [str(a + b - 10), str(a + b + 10), str(a + b + 1)]

def g2_sub():
    a, b = rng.randint(52, 95), rng.randint(17, 48)
    return f"What is {a} minus {b}?", str(a - b), [str(a - b + 10), str(a - b - 10), str(a - b + 2)]

def g2_hundreds():
    d = rng.sample(range(1, 10), 3)
    n = d[0] * 100 + d[1] * 10 + d[2]
    return f"In the number {n}, what digit is in the hundreds place?", str(d[0]), [str(d[1]), str(d[2]), str(n)]

def g2_money():
    di, ni = rng.randint(1, 5), rng.randint(1, 4)
    ans = 10 * di + 5 * ni
    dimes = f"{di} dime" + ("s" if di > 1 else "")
    nickels = f"{ni} nickel" + ("s" if ni > 1 else "")
    return (f"How many cents are {dimes} and {nickels}?", str(ans),
            [str(di + ni), str(10 * di + ni), str(5 * di + 10 * ni)] if 5 * di + 10 * ni != ans else [str(di + ni), str(10 * di + ni), str(ans + 5)])

def g3_mul():
    a, b = rng.randint(3, 9), rng.randint(3, 9)
    return f"What is {a} times {b}?", str(a * b), list({str(a * b + a), str(a * b - b), str(a + b)} - {str(a * b)})[:3] or num_distractors(a * b)

def g3_div():
    a, b = rng.randint(3, 9), rng.randint(3, 9)
    return f"What is {a * b} divided by {b}?", str(a), num_distractors(a, spread=3)

def g3_area():
    l, w = rng.randint(3, 9), rng.randint(2, 8)
    return (f"A rectangle is {l} units long and {w} units wide. What is its area in square units?",
            str(l * w), list({str(2 * (l + w)), str(l + w), str(l * w + l)} - {str(l * w)})[:3])

def g3_round():
    n = rng.randint(11, 98)
    while n % 10 == 5 or n % 10 == 0:
        n = rng.randint(11, 98)
    r = int(round(n, -1))
    return f"What is {n} rounded to the nearest ten?", str(r), [str(r + 10), str(r - 10), str(n)]

def g4_mul():
    a, b = rng.randint(12, 39), rng.randint(11, 19)
    return f"What is {a} times {b}?", str(a * b), [str(a * b + 10), str(a * b - a), str(a * (b - 10) + 10 * a + 10)]

def g4_factor():
    n = rng.choice([24, 30, 36, 42, 48])
    fac = rng.choice([d for d in range(3, n // 2 + 1) if n % d == 0])
    non = rng.sample([d for d in range(3, 15) if n % d], 3)
    return f"Which number is a factor of {n}?", str(fac), [str(x) for x in non]

def g4_frac():
    d = rng.choice([5, 7, 8, 9]); a = rng.randint(1, 3); b = rng.randint(1, d - a - 1)
    return (f"What is {a}/{d} plus {b}/{d}?", f"{a + b}/{d}",
            [f"{a + b}/{2 * d}", f"{a + b + 1}/{d}", f"{a + b - 1}/{d}"])

def g4_perim():
    l, w = rng.randint(6, 15), rng.randint(3, 9)
    return (f"A rectangle is {l} cm long and {w} cm wide. What is its perimeter in cm?",
            str(2 * (l + w)), list({str(l * w), str(l + w), str(2 * l + w)} - {str(2 * (l + w))})[:3])

def g5_pow10():
    e = rng.randint(2, 5)
    return f"What is 10 to the power of {e}?", str(10 ** e), [str(10 * e), str(10 ** (e - 1)), str(10 ** (e + 1))]

def g5_fracof():
    d = rng.choice([3, 4, 5]); n = rng.randint(1, d - 1); w = d * rng.randint(3, 8)
    ans = n * w // d
    return f"What is {n}/{d} of {w}?", str(ans), list({str(w // d), str(w - ans), str(ans + d)} - {str(ans)})[:3]

def g5_volume():
    l, w, h = rng.randint(2, 6), rng.randint(2, 6), rng.randint(2, 5)
    return (f"A box is {l} cm long, {w} cm wide and {h} cm tall. What is its volume in cubic cm?",
            str(l * w * h), list({str(l + w + h), str(l * w), str(l * w * h + l * w)} - {str(l * w * h)})[:3])

def g5_dec():
    a = rng.choice([x for x in range(11, 50) if x % 10]) / 10
    b = rng.choice([x for x in range(101, 400) if x % 10]) / 100
    ans = round(a + b, 2)
    # distractors: off by one, off by a tenth, and misaligned place values (e.g. 2.5 + 1.75 -> 1.0)
    misaligned = round(b + int(a * 10) / 100, 2)
    return (f"What is {a:g} plus {b:g}?", f"{ans:g}",
            [f"{round(ans + 1, 2):g}", f"{round(ans - 0.1, 2):g}", f"{misaligned:g}"])

def g6_pow():
    b, e = rng.randint(2, 5), rng.randint(2, 4)
    ans = b ** e
    return f"What is {b} to the power of {e}?", str(ans), list({str(b * e), str(b + e), str(b ** (e - 1))} - {str(ans)})[:3]

def g6_pct():
    p = rng.choice([10, 20, 25, 50, 75]); w = rng.choice([40, 60, 80, 120, 200])
    ans = p * w // 100
    return f"What is {p} percent of {w}?", str(ans), list({str(p + w), str(w - ans), str(ans * 2)} - {str(ans)})[:3]

def g6_neg():
    nums = rng.sample(range(-9, 10), 4)
    while sum(x < 0 for x in nums) < 2:
        nums = rng.sample(range(-9, 10), 4)
    return (f"Which number is the smallest: {', '.join(map(str, nums))}?",
            str(min(nums)), [str(x) for x in nums if x != min(nums)])

def g6_onestep():
    x, a = rng.randint(3, 20), rng.randint(2, 15)
    return f"If x plus {a} equals {x + a}, what is x?", str(x), list({str(x + a), str(x + 2 * a), str(x + 1)} - {str(x)})[:3]

def g7_mulint():
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    return f"What is -{a} times {b}?", str(-a * b), [str(a * b), str(-a - b), str(b - a) if b - a != -a * b else str(-a * b - 1)]

def g7_addint():
    a, b = rng.randint(5, 15), rng.randint(2, 9)
    ans = -a + b
    return f"What is -{a} plus {b}?", str(ans), list({str(a + b), str(-a - b), str(-ans)} - {str(ans)})[:3]

def g7_twostep():
    x, a, c = rng.randint(2, 9), rng.randint(2, 6), rng.randint(1, 12)
    return (f"If {a}x plus {c} equals {a * x + c}, what is x?", str(x),
            list({str(a * x + c - c), str(x + c), str(x + 1)} - {str(x)})[:3])

def g7_prob():
    k = rng.randint(2, 6)
    ans = Fraction(k - 1, 6)
    cands = [Fraction(k, 6), Fraction(1, k), Fraction(7 - k, 6), Fraction(1, 6), Fraction(k - 1, 12), Fraction(1, 2)]
    wrong = list(dict.fromkeys(str(c) for c in cands if c != ans and c < 1))
    return (f"A fair six-sided die is rolled once. What is the probability of rolling a number less than {k}?",
            str(ans), wrong[:3])

def g8_sqrt():
    r = rng.randint(4, 15)
    return f"What is the square root of {r * r}?", str(r), list({str(r * r // 2), str(r + 1), str(2 * r)} - {str(r)})[:3]

G8_TRIPLES = iter([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)])
def g8_pyth():
    a, b, c = next(G8_TRIPLES)
    return (f"A right triangle has legs of length {a} and {b}. How long is the longest side?",
            str(c), list({str(a + b), str(b + 1), str(c + 2)} - {str(c)})[:3])

def g8_exprule():
    b, m, n = rng.randint(2, 5), rng.randint(2, 6), rng.randint(2, 6)
    while m == n:
        n = rng.randint(2, 6)
    return (f"{b} to the power of {m} times {b} to the power of {n} equals {b} to the power of what?",
            str(m + n), list({str(m * n), str(abs(m - n)), str(m + n + 1)} - {str(m + n)})[:3])

def g8_slope():
    b, m = rng.randint(-3, 5), rng.randint(2, 5)
    x2 = rng.randint(1, 4)
    return (f"What is the slope of the line through the points (0, {b}) and ({x2}, {b + m * x2})?",
            str(m), list({str(b + m * x2), str(x2), str(-m)} - {str(m)})[:3])

MATH = [
    (0, "K.OA.A.5", "addition", k_add), (0, "K.CC.A.2", "counting", k_next),
    (0, "K.CC.C.7", "comparing numbers", k_greatest), (0, "K.G.B.4", "geometry", k_shape),
    (1, "1.OA.C.6", "addition", g1_add), (1, "1.OA.C.6s", "subtraction", g1_sub),
    (1, "1.NBT.B.2", "place value", g1_tens), (1, "1.NBT.C.4", "addition", g1_add10),
    (2, "2.NBT.B.5", "addition", g2_add), (2, "2.NBT.B.5s", "subtraction", g2_sub),
    (2, "2.NBT.A.1", "place value", g2_hundreds), (2, "2.MD.C.8", "measurement", g2_money),
    (3, "3.OA.C.7", "multiplication", g3_mul), (3, "3.OA.C.7d", "division", g3_div),
    (3, "3.MD.C.7", "geometry", g3_area), (3, "3.NBT.A.1", "place value", g3_round),
    (4, "4.NBT.B.5", "multiplication", g4_mul), (4, "4.OA.B.4", "factors", g4_factor),
    (4, "4.NF.B.3", "fractions", g4_frac), (4, "4.MD.A.3", "geometry", g4_perim),
    (5, "5.NBT.A.2", "exponents", g5_pow10), (5, "5.NF.B.4", "fractions", g5_fracof),
    (5, "5.MD.C.5", "geometry", g5_volume), (5, "5.NBT.B.7", "decimals", g5_dec),
    (6, "6.EE.A.1", "exponents", g6_pow), (6, "6.RP.A.3c", "percent", g6_pct),
    (6, "6.NS.C.7", "negative numbers", g6_neg), (6, "6.EE.B.7", "equations", g6_onestep),
    (7, "7.NS.A.2", "negative numbers", g7_mulint), (7, "7.NS.A.1", "negative numbers", g7_addint),
    (7, "7.EE.B.4a", "equations", g7_twostep), (7, "7.SP.C.7", "probability", g7_prob),
    (8, "8.EE.A.2", "roots", g8_sqrt), (8, "8.G.B.7", "geometry", g8_pyth),
    (8, "8.EE.A.1", "exponents", g8_exprule), (8, "8.F.B.4", "equations", g8_slope),
]
for grade, std, topic, fn in MATH:
    math_gen(grade, std, topic, 4, fn)

# ---------------------------------------------------------------- science
# (grade, standard, topic, question, correct, [wrong x3])
SCIENCE = [
    # K
    (0, "K-LS1-1", "life science", "What do plants need to grow?", "water", ["plastic", "salt", "rocks"]),
    (0, "K-PS2-1", "forces", "What can make a ball start rolling?", "a push", ["a color", "a sound", "a shadow"]),
    (0, "K-PS3-1", "energy", "On a sunny day, the sun makes a sidewalk feel", "warmer", ["colder", "wetter", "softer"]),
    (0, "K-LS1-1", "life science", "What do animals need to live?", "food", ["toys", "paper", "paint"]),
    (0, "K-ESS2-1", "earth science", "When it rains, what falls from the clouds?", "water", ["sand", "rocks", "leaves"]),
    (0, "K-PS2-1", "forces", "If you pull on a door handle, the door will", "open", ["sing", "grow", "melt"]),
    (0, "K-ESS2-1", "earth science", "What should you wear when it is very cold outside?", "a coat", ["shorts", "sandals", "a swimsuit"]),
    (0, "K-LS1-1", "life science", "What does a bird use to fly?", "wings", ["roots", "leaves", "fins"]),
    (0, "K-ESS3-1", "earth science", "Where does a fish live?", "in water", ["in a tree", "in the sand", "in the sky"]),
    (0, "K-PS3-2", "energy", "What can keep you cool on a hot, sunny day?", "shade", ["a fire", "a blanket", "a heater"]),
    (0, "K-ESS2-2", "earth science", "A squirrel digs a hole in the ground to hide", "nuts", ["rocks", "shoes", "books"]),
    (0, "K-ESS2-1", "earth science", "Which season is usually the coldest?", "winter", ["summer", "spring", "fall"]),
    # 1
    (1, "1-PS4-1", "waves", "When you pluck a guitar string, the string", "shakes", ["melts", "grows", "glows"]),
    (1, "1-PS4-2", "waves", "What do you need to see things in a dark room?", "light", ["sound", "water", "wind"]),
    (1, "1-ESS1-1", "space", "In the morning, the sun rises in the", "east", ["west", "north", "south"]),
    (1, "1-ESS1-1", "space", "Which can you often see in the night sky?", "stars", ["the sun", "rainbows", "a sunrise"]),
    (1, "1-LS3-1", "life science", "A baby duck looks most like", "its parents", ["a cat", "a frog", "a fish"]),
    (1, "1-LS1-1", "life science", "What part of a plant takes in water from the soil?", "the roots", ["the petals", "the seeds", "the fruit"]),
    (1, "1-PS4-3", "waves", "Light cannot pass through", "a wooden door", ["clear glass", "clear water", "air"]),
    (1, "1-LS1-1", "life science", "What does a turtle use to protect itself?", "its shell", ["its tail", "its eyes", "its feet"]),
    (1, "1-ESS1-2", "space", "In which season are the days longest?", "summer", ["winter", "fall", "spring"]),
    (1, "1-PS4-3", "waves", "When light hits a mirror, the mirror", "bounces it back", ["makes it hot", "turns it off", "makes it loud"]),
    (1, "1-LS1-2", "life science", "Baby birds chirp loudly so that their parents will", "feed them", ["sleep", "swim", "fly away"]),
    (1, "1-LS1-1", "life science", "What does a cactus have to protect it from animals?", "spines", ["fur", "wings", "scales"]),
    # 2
    (2, "2-PS1-4", "matter", "When ice is heated, it", "melts", ["freezes", "grows", "turns to sand"]),
    (2, "2-PS1-4", "matter", "When water is put in a freezer, it", "turns to ice", ["boils", "turns to steam", "disappears"]),
    (2, "2-LS2-2", "life science", "When bees visit flowers, they carry", "pollen", ["water", "dirt", "leaves"]),
    (2, "2-PS1-2", "matter", "Which material is best for making a window?", "glass", ["wood", "clay", "cloth"]),
    (2, "2-PS1-1", "matter", "Which of these is a liquid?", "milk", ["a rock", "a pencil", "a coin"]),
    (2, "2-ESS2-1", "earth science", "Over a long time, wind and water slowly change the shape of", "the land", ["the sun", "the moon", "the stars"]),
    (2, "2-ESS1-1", "earth science", "Which change happens very fast?", "a volcano erupting", ["a canyon forming", "a mountain wearing down", "a river carving a valley"]),
    (2, "2-ESS2-3", "earth science", "Where is most of the water on Earth?", "in the oceans", ["in lakes", "in rivers", "in clouds"]),
    (2, "2-LS2-2", "life science", "Some seeds stick to an animal's fur. This helps the seeds", "move to new places", ["turn into rocks", "make more fur", "stop growing"]),
    (2, "2-PS1-1", "matter", "Which object is the hardest?", "a rock", ["a pillow", "a sponge", "a cotton ball"]),
    (2, "2-PS1-4", "matter", "Which change can be undone?", "freezing water", ["baking bread", "burning paper", "cooking an egg"]),
    (2, "2-LS4-1", "life science", "A dry place with very little rain and lots of sand is a", "desert", ["rainforest", "pond", "ocean"]),
    # 3
    (3, "3-PS2-3", "forces", "A magnet will pull on", "a steel paper clip", ["a plastic cup", "a wooden block", "a rubber band"]),
    (3, "3-PS2-3", "forces", "When the north poles of two magnets face each other, the magnets", "push apart", ["pull together", "melt", "get warm"]),
    (3, "3-LS1-1", "life science", "In a frog's life cycle, what comes right after the egg?", "a tadpole", ["an adult frog", "a caterpillar", "a pupa"]),
    (3, "3-LS4-1", "life science", "Remains of plants and animals from long ago found in rock are called", "fossils", ["minerals", "crystals", "magnets"]),
    (3, "3-LS4-3", "life science", "A thick coat of fur helps an animal live where it is", "very cold", ["very hot", "very dry", "very windy"]),
    (3, "3-ESS2-1", "earth science", "Which tool measures how hot or cold the air is?", "a thermometer", ["a ruler", "a scale", "a compass"]),
    (3, "3-PS2-1", "forces", "Two teams pull on a rope equally hard. The rope will", "stay still", ["move to the left", "move to the right", "spin around"]),
    (3, "3-LS3-1", "life science", "Young animals get traits like eye color from their", "parents", ["food", "friends", "home"]),
    (3, "3-ESS3-1", "earth science", "A wall built along the shore protects a town mostly from", "floods", ["earthquakes", "tornadoes", "droughts"]),
    (3, "3-LS1-1", "life science", "A caterpillar grows up to become a", "butterfly", ["beetle", "bee", "spider"]),
    (3, "3-ESS2-2", "earth science", "The kind of weather a place has over many years is called its", "climate", ["season", "forecast", "temperature"]),
    (3, "3-LS3-2", "life science", "Which of these is learned, not passed down from parents?", "riding a bike", ["eye color", "hair color", "number of fingers"]),
    # 4
    (4, "4-PS3-1", "energy", "Compared with a slow ball, a fast ball of the same size has", "more energy", ["less energy", "no energy", "the same energy"]),
    (4, "4-ESS3-1", "energy", "Which energy source will not run out?", "wind", ["coal", "oil", "natural gas"]),
    (4, "4-PS4-2", "waves", "We see an object when light", "bounces off it and enters our eyes", ["leaves our eyes and hits it", "is blocked by our eyes", "turns into sound"]),
    (4, "4-ESS2-1", "earth science", "Breaking rock into smaller pieces by wind, water, or ice is called", "weathering", ["melting", "freezing", "growing"]),
    (4, "4-PS3-4", "energy", "A flashlight changes the energy stored in its battery into", "light", ["wind", "water", "rock"]),
    (4, "4-ESS1-1", "earth science", "In layers of rock, the oldest layer is usually at the", "bottom", ["top", "middle", "side"]),
    (4, "4-PS4-1", "waves", "The highest point of a water wave is called the", "crest", ["root", "stem", "shell"]),
    (4, "4-ESS3-1", "energy", "Which energy source comes from the remains of ancient living things?", "coal", ["wind", "sunlight", "moving water"]),
    (4, "4-LS1-1", "life science", "The main job of an animal's heart is to", "pump blood", ["digest food", "breathe air", "see light"]),
    (4, "4-PS4-1", "waves", "Sound travels from place to place as a", "wave", ["liquid", "metal", "plant"]),
    (4, "4-PS3-3", "energy", "When two moving cars crash, some of their energy changes into", "sound and heat", ["ice and snow", "seeds and soil", "water and salt"]),
    (4, "4-LS1-1", "life science", "Which part of a plant makes seeds?", "the flower", ["the root", "the stem", "the bark"]),
    # 5
    (5, "5-PS2-1", "forces", "Gravity pulls objects", "down toward Earth", ["up toward the sky", "toward the moon", "sideways"]),
    (5, "5-LS1-1", "life science", "Plants get most of the material they need to grow from", "air and water", ["soil only", "sunlight only", "rocks"]),
    (5, "5-PS3-1", "energy", "The energy in the food animals eat first came from", "the sun", ["the soil", "water", "the moon"]),
    (5, "5-LS2-1", "life science", "Living things that break down dead plants and animals are called", "decomposers", ["producers", "predators", "herbivores"]),
    (5, "5-ESS1-2", "space", "Earth spinning on its axis causes", "day and night", ["the seasons", "the tides", "earthquakes"]),
    (5, "5-ESS1-1", "space", "The sun looks brighter than other stars because it is", "closer to Earth", ["the biggest star", "the hottest star", "the youngest star"]),
    (5, "5-PS1-2", "matter", "When sugar dissolves in water, the total weight", "stays the same", ["goes down", "goes to zero", "doubles"]),
    (5, "5-PS1-4", "matter", "Salt water is an example of a", "mixture", ["solid", "gas", "metal"]),
    (5, "5-ESS2-2", "earth science", "Most of Earth's fresh water is frozen in", "glaciers and ice caps", ["the oceans", "rivers", "clouds"]),
    (5, "5-LS2-1", "life science", "In the food chain grass, rabbit, fox, the rabbit is eaten by the", "fox", ["grass", "sun", "soil"]),
    (5, "5-ESS1-2", "space", "On a sunny day, your shadow is longest", "in the early morning", ["at noon", "when it rains", "at midnight"]),
    (5, "5-PS1-1", "matter", "When more air is pumped into a ball, the ball", "gets bigger", ["gets smaller", "turns to water", "gets lighter"]),
    # 6 (CA integrated: cells, body systems, thermal energy, weather, climate)
    (6, "MS-LS1-1", "life science", "The basic unit of all living things is the", "cell", ["organ", "tissue", "bone"]),
    (6, "MS-LS1-2", "life science", "Which part of a cell holds its DNA and controls its activities?", "the nucleus", ["the cell membrane", "the cell wall", "the vacuole"]),
    (6, "MS-LS1-2", "life science", "Which part do plant cells have that animal cells do not?", "a cell wall", ["a nucleus", "a cell membrane", "cytoplasm"]),
    (6, "MS-PS3-3", "energy", "Heat moving from a hot pan into your hand by touch is called", "conduction", ["convection", "radiation", "evaporation"]),
    (6, "MS-ESS2-4", "earth science", "Water vapor cooling into liquid droplets in clouds is called", "condensation", ["evaporation", "precipitation", "transpiration"]),
    (6, "MS-ESS2-6", "earth science", "Warm air rises because it is", "less dense than cool air", ["heavier than cool air", "wetter than cool air", "darker than cool air"]),
    (6, "MS-LS1-3", "life science", "A group of organs that work together, like the heart and blood vessels, is an", "organ system", ["organelle", "molecule", "atom"]),
    (6, "MS-ESS3-5", "earth science", "Gases like carbon dioxide that trap heat in the atmosphere are called", "greenhouse gases", ["noble gases", "ideal gases", "inert gases"]),
    (6, "MS-PS3-3", "energy", "Which material is the best insulator?", "foam", ["copper", "aluminum", "iron"]),
    (6, "MS-ESS2-5", "earth science", "A large body of air with similar temperature and humidity is an", "air mass", ["air pump", "air bubble", "air pocket"]),
    (6, "MS-LS1-3", "life science", "The body system that breaks food down into nutrients is the", "digestive system", ["nervous system", "skeletal system", "respiratory system"]),
    (6, "MS-PS3-4", "energy", "The total thermal energy of an object depends on its temperature and its", "amount of matter", ["color", "shape", "smell"]),
    # 7 (CA integrated: atoms and reactions, photosynthesis and respiration, ecosystems, rock cycle)
    (7, "MS-LS1-6", "life science", "Plants make sugar from carbon dioxide and water in a process called", "photosynthesis", ["respiration", "digestion", "fermentation"]),
    (7, "MS-LS1-7", "life science", "Cells release energy from sugar using oxygen in a process called", "cellular respiration", ["photosynthesis", "transpiration", "condensation"]),
    (7, "MS-PS1-1", "matter", "The smallest unit of an element that keeps its properties is an", "atom", ["organ", "cell", "crystal"]),
    (7, "MS-PS1-1", "matter", "The formula H2O means a water molecule has", "two hydrogen atoms and one oxygen atom", ["one hydrogen atom and two oxygen atoms", "two hydrogen atoms and two oxygen atoms", "one hydrogen atom and one oxygen atom"]),
    (7, "MS-PS1-2", "matter", "Iron rusting forms a new substance. This is a", "chemical change", ["physical change", "change of state", "change of shape"]),
    (7, "MS-PS1-5", "matter", "During a chemical reaction, atoms are", "rearranged into new substances", ["destroyed", "created from nothing", "turned into light"]),
    (7, "MS-ESS2-1", "earth science", "Rock that forms when magma or lava cools is called", "igneous rock", ["sedimentary rock", "metamorphic rock", "river rock"]),
    (7, "MS-LS2-2", "life science", "Two species that need the same limited food are in", "competition", ["mutualism", "parasitism", "camouflage"]),
    (7, "MS-LS1-6", "life science", "Oxygen gas is released as a product of", "photosynthesis", ["cellular respiration", "digestion", "burning wood"]),
    (7, "MS-LS2-3", "life science", "Less energy is available at each higher level of a food pyramid because much is lost as", "heat", ["water", "light", "soil"]),
    (7, "MS-PS1-1", "matter", "A substance made of two or more elements chemically joined is a", "compound", ["mixture", "solution", "metal"]),
    (7, "MS-PS1-1", "matter", "What is the chemical formula of carbon dioxide?", "CO2", ["H2O", "O2", "NaCl"]),
    # 8 (CA integrated: forces and motion, waves, genetics, evolution, space)
    (8, "MS-ESS1-1", "space", "Earth has seasons mainly because of", "the tilt of Earth's axis", ["Earth's distance from the sun", "Earth spinning each day", "clouds blocking the sun"]),
    (8, "MS-PS2-2", "forces", "An object at rest stays at rest unless an unbalanced force acts on it. This is Newton's", "first law", ["second law", "third law", "law of gravity"]),
    (8, "MS-PS2-2", "forces", "Newton's second law says that force equals mass times", "acceleration", ["speed", "volume", "weight"]),
    (8, "MS-PS2-1", "forces", "Newton's third law says that for every action there is an equal and opposite", "reaction", ["motion", "speed", "mass"]),
    (8, "MS-LS3-1", "life science", "A change in the DNA sequence of a gene is called a", "mutation", ["fertilization", "pollination", "germination"]),
    (8, "MS-LS4-4", "life science", "Individuals with helpful traits survive and reproduce more. This process is called", "natural selection", ["cell division", "pollination", "weathering"]),
    (8, "MS-ESS1-1", "space", "The phases of the moon are caused by", "how much of its sunlit side we see", ["Earth's shadow covering it", "clouds in front of it", "the moon changing shape"]),
    (8, "MS-PS4-1", "waves", "The distance from one wave crest to the next is the", "wavelength", ["amplitude", "frequency", "speed"]),
    (8, "MS-PS2-4", "forces", "The pull of gravity between two objects depends on their masses and their", "distance apart", ["colors", "temperatures", "shapes"]),
    (8, "MS-LS3-1", "life science", "Genes are found on structures called", "chromosomes", ["ribosomes", "chloroplasts", "vacuoles"]),
    (8, "MS-PS4-3", "waves", "Which kind of wave can travel through empty space?", "light", ["sound", "ocean waves", "waves on a rope"]),
    (8, "MS-ESS1-4", "earth science", "About how old is Earth?", "4.6 billion years", ["6 thousand years", "46 million years", "460 years"]),
]
for i, (grade, std, topic, q, correct, wrong) in enumerate(SCIENCE):
    add(grade, "science", topic, std, q, correct, wrong, i)

assert len({it["id"] for it in items}) == len(items)
out = sys.argv[1] if len(sys.argv) > 1 else "items.jsonl"
with open(out, "w") as f:
    for it in items:
        f.write(json.dumps(it) + "\n")
print(f"wrote {len(items)} items to {out}")
