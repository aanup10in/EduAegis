/**
 * EduAegis Comprehensive Curriculum Database
 * Covers Classes 8, 9, 10 with primary depth in Class 9 (Physics, Chemistry, Biology, Mathematics).
 * Aligned with CBSE, ICSE, and State Board standards.
 */

export interface ConceptDetail {
  id: string;
  name: string;
  summary: string;
  teacherExplanation: string;
  audioScript: string;
  analogies: string[];
  examples: {
    title: string;
    scenario: string;
    explanation: string;
  }[];
  keyFormulas: string[];
  commonMisconceptions: string[];
  authenticReferences: {
    title: string;
    url: string;
    source: string;
  }[];
}

export interface Chapter {
  id: string;
  title: string;
  ncertChapter: string;
  description: string;
  concepts: ConceptDetail[];
  practiceExamples: {
    id: string;
    question: string;
    maxMarks: number;
    hiddenSolution: {
      steps: { stepNumber: number; description: string; marks: number }[];
      finalAnswer: string;
      keyInsight: string;
    };
  }[];
  subjectivePaper: {
    id: string;
    question: string;
    maxMarks: number;
    questionType: "Short Definition" | "Conceptual Reasoning" | "Derivation / Numerical";
    modelAnswer: string;
    rubricPoints: string[];
  }[];
}

export interface Subject {
  id: string;
  name: string;
  icon: string;
  accentColor: string;
  chapters: Chapter[];
}

export interface ClassCurriculum {
  className: string;
  classNumber: number;
  subjects: Subject[];
}

export const CURRICULUM_DATA: Record<number, ClassCurriculum> = {
  9: {
    className: "Class 9th (Secondary)",
    classNumber: 9,
    subjects: [
      {
        id: "physics",
        name: "Physics",
        icon: "Atom",
        accentColor: "from-blue-600 to-indigo-700",
        chapters: [
          {
            id: "force_and_laws",
            title: "Force and Laws of Motion",
            ncertChapter: "NCERT Class 9 - Chapter 8",
            description: "Study unbalanced forces, inertia, momentum, Newton's three laws of motion, and conservation of momentum.",
            concepts: [
              {
                id: "newton_second_law",
                name: "Newton's Second Law & Momentum (F = ma)",
                summary: "The rate of change of momentum of an object is directly proportional to the applied unbalanced force and takes place in the direction of the force.",
                teacherExplanation: "Hello! Let's understand Newton's Second Law in simple terms. Imagine you are in a cricket match. When a fast cricket ball comes towards you, catching it hurts your hand if you stop it instantly. But if you pull your hands backward, you take more time to stop the ball, reducing the force! That's momentum and Newton's Second Law in real life. Force equals mass times acceleration (F = ma).",
                audioScript: "Hello student! Welcome to EduAegis Physics class. Today we are mastering Newton's Second Law of Motion. First, what is momentum? Momentum is mass in motion: p equals m times v. Newton discovered that when you push something, the change in its momentum depends directly on the force applied and the time taken. By pulling your hands back while catching a cricket ball, you increase time, which reduces the force on your palms. Remember the golden formula: Force equals mass times acceleration, F equals m a, measured in Newtons.",
                analogies: [
                  "Catching a fast cricket ball: pulling hands back increases time 't', reducing impact force 'F'.",
                  "High jump athletes landing on soft foam or sand cushions to increase deceleration time.",
                  "Seatbelts in cars stretching slightly during sudden braking to prolong stopping time."
                ],
                examples: [
                  {
                    title: "Example 1: A Pushed Shopping Cart",
                    scenario: "A 20 kg empty shopping cart is accelerated at 2 m/s². What force was applied?",
                    explanation: "Using F = m * a: Mass m = 20 kg, acceleration a = 2 m/s². Force = 20 * 2 = 40 Newtons (N). If you double the mass by loading 20 kg groceries, the same 40 N force will only produce an acceleration of 1 m/s²."
                  },
                  {
                    title: "Example 2: Why Karate Fighters Break Bricks",
                    scenario: "A karate expert strikes a pile of tiles with very high speed in a tiny fraction of a second.",
                    explanation: "The mass of the hand is moderate, but the velocity drops from high speed to zero in a tiny fraction of a second (t ≈ 0.01 s). Because Δt is extremely small, the rate of change of momentum is enormous, delivering a massive breaking force."
                  }
                ],
                keyFormulas: [
                  "Momentum: p = m * v (SI unit: kg·m/s)",
                  "Force: F = Δp / Δt = m(v - u) / t",
                  "Newton's Second Law: F = m * a (SI unit: Newton, 1 N = 1 kg·m/s²)"
                ],
                commonMisconceptions: [
                  "Confusing Newton's 2nd Law (rate of change of momentum) with 3rd Law (action-reaction).",
                  "Assuming force is needed to maintain motion; an object in uniform motion needs zero net force.",
                  "Writing the SI unit of force as Joules (energy) instead of Newtons (N)."
                ],
                authenticReferences: [
                  {
                    title: "NCERT Class 9 Physics - Force & Laws of Motion (Official Textbook)",
                    url: "https://ncert.nic.in/textbook.php?iesc1=8-15",
                    source: "NCERT Official Portal"
                  },
                  {
                    title: "Khan Academy: Newton's Second Law of Motion",
                    url: "https://www.khanacademy.org/science/in-in-class9th-physics-india/in-in-forces-and-laws-of-motion",
                    source: "Khan Academy India"
                  },
                  {
                    title: "HyperPhysics - Georgia State University: Newton's Laws",
                    url: "http://hyperphysics.phy-astr.gsu.edu/hbase/newt.html",
                    source: "HyperPhysics Educational Database"
                  }
                ]
              },
              {
                id: "inertia_first_law",
                name: "Inertia and Newton's First Law",
                summary: "An object remains in a state of rest or uniform motion in a straight line unless acted upon by an external unbalanced force.",
                teacherExplanation: "Inertia is simply the stubbornness of matter! An object at rest wants to stay at rest; an object moving wants to keep moving. When a bus suddenly accelerates forward, your feet move forward with the bus floor, but your upper body wants to stay at rest, so you jerk backward. Mass is the measure of inertia.",
                audioScript: "Newton's First Law is also known as the Law of Inertia. Inertia is the natural tendency of any object to resist changes in its state of rest or motion. Heavier objects have more inertia. That is why it is harder to push a stalled truck than a bicycle.",
                analogies: [
                  "Jerking backward when a stationary bus suddenly starts moving forward.",
                  "Falling forward when a running bus suddenly hits the brakes.",
                  "Dust falling off a carpet when beaten with a stick."
                ],
                examples: [
                  {
                    title: "Example: Coin and Card on a Glass",
                    scenario: "A playing card is placed over a glass tumbler and a 5-rupee coin rests on it. When the card is flicked sharply with a finger, the card flies away but the coin drops into the glass.",
                    explanation: "The sharp flick exerts force only on the card. The coin, due to its inertia of rest, remains in place and gravity pulls it straight down into the tumbler."
                  }
                ],
                keyFormulas: [
                  "Inertia ∝ Mass (Mass is quantitative measure of inertia)",
                  "Net Force ΣF = 0 implies acceleration a = 0"
                ],
                commonMisconceptions: [
                  "Believing inertia is a force (Inertia is an inherent property, not a force).",
                  "Thinking an object stops on its own because its inertia runs out (it stops because of friction)."
                ],
                authenticReferences: [
                  {
                    title: "NCERT Chapter 8: Inertia and Mass",
                    url: "https://ncert.nic.in/textbook.php?iesc1=8-15",
                    source: "NCERT"
                  }
                ]
              }
            ],
            practiceExamples: [
              {
                id: "ex_1",
                question: "A constant force acts on an object of mass 5 kg for a duration of 2 seconds. It increases the object's velocity from 3 m/s to 7 m/s. Find the magnitude of the applied force. If the force was applied for a duration of 5 seconds, what would be the final velocity?",
                maxMarks: 4,
                hiddenSolution: {
                  steps: [
                    { stepNumber: 1, description: "Identify given parameters: mass m = 5 kg, initial velocity u = 3 m/s, final velocity v = 7 m/s, time t = 2 s.", marks: 1 },
                    { stepNumber: 2, description: "Calculate acceleration: a = (v - u) / t = (7 - 3) / 2 = 4 / 2 = 2 m/s².", marks: 1 },
                    { stepNumber: 3, description: "Calculate force using Newton's Second Law: F = m * a = 5 kg * 2 m/s² = 10 N.", marks: 1 },
                    { stepNumber: 4, description: "Compute final velocity when time t' = 5 s: v' = u + a * t' = 3 + (2 * 5) = 3 + 10 = 13 m/s.", marks: 1 }
                  ],
                  finalAnswer: "Applied Force = 10 Newtons; Final Velocity after 5 s = 13 m/s.",
                  keyInsight: "Force remains constant, so acceleration is constant throughout the motion."
                }
              },
              {
                id: "ex_2",
                question: "Which would require a greater force: accelerating a 2 kg mass at 5 m/s² or a 4 kg mass at 2 m/s²?",
                maxMarks: 3,
                hiddenSolution: {
                  steps: [
                    { stepNumber: 1, description: "For first body: m1 = 2 kg, a1 = 5 m/s². Force F1 = m1 * a1 = 2 * 5 = 10 N.", marks: 1 },
                    { stepNumber: 2, description: "For second body: m2 = 4 kg, a2 = 2 m/s². Force F2 = m2 * a2 = 4 * 2 = 8 N.", marks: 1 },
                    { stepNumber: 3, description: "Compare magnitudes: F1 (10 N) > F2 (8 N). Conclude that accelerating the 2 kg mass at 5 m/s² requires more force.", marks: 1 }
                  ],
                  finalAnswer: "Accelerating the 2 kg mass at 5 m/s² requires a greater force (10 N vs 8 N).",
                  keyInsight: "Force depends on the product of both mass and acceleration, not mass alone."
                }
              }
            ],
            subjectivePaper: [
              {
                id: "q1",
                question: "State Newton's Second Law of Motion. Derive the mathematical expression F = ma from this law, defining all terms with their SI units.",
                maxMarks: 5,
                questionType: "Derivation / Numerical",
                modelAnswer: "Newton's Second Law of Motion states that the rate of change of momentum of an object is directly proportional to the applied unbalanced force, and takes place in the direction of the force.\n\nDerivation:\nLet mass of the object be 'm', initial velocity 'u', and final velocity 'v' after time 't' under force 'F'.\nInitial momentum p1 = m * u\nFinal momentum p2 = m * v\nChange in momentum Δp = p2 - p1 = m(v - u)\nRate of change of momentum = m(v - u) / t\nBy Newton's 2nd Law: F ∝ m(v - u) / t\nSince acceleration a = (v - u) / t:\nF ∝ m * a => F = k * m * a\nIn SI units, choosing k = 1: F = m * a.\nSI Units: Force in Newton (N), mass in kg, acceleration in m/s².",
                rubricPoints: [
                  "1.0 mark: Exact statement of Newton's 2nd Law (rate of change of momentum proportional to unbalanced force in its direction).",
                  "2.0 marks: Step-by-step derivation: p1=mu, p2=mv, Δp=m(v-u), rate of change = m(v-u)/t.",
                  "1.0 mark: Substituting a = (v-u)/t to get F = k*m*a, explaining why k=1 in SI.",
                  "1.0 mark: Correct SI units for all quantities (Force in N, mass in kg, acceleration in m/s²)."
                ]
              },
              {
                id: "q2",
                question: "Why does a fielder pull his hands backward while catching a fast-moving cricket ball? Explain the physical mechanism using Newton's Second Law.",
                maxMarks: 3,
                questionType: "Conceptual Reasoning",
                modelAnswer: "When a fielder pulls his hands backward while catching a cricket ball, he increases the time duration 't' over which the high velocity of the ball is reduced to zero. According to Newton's Second Law, Force F = m(v - u) / t. Since the change in momentum m(v - u) is constant, increasing the time 't' decreases the rate of change of momentum. Consequently, a much smaller impact force is exerted on the fielder's palms, preventing injury.",
                rubricPoints: [
                  "1.0 mark: Mentions that pulling hands back increases the time taken to bring ball's velocity to zero.",
                  "1.0 mark: Applies Newton's 2nd Law formula F = m(v-u)/t showing inverse relationship between force and time.",
                  "1.0 mark: Concludes that smaller stopping force acts on the hands, preventing pain or injury."
                ]
              },
              {
                id: "q3",
                question: "Define Inertia. State its three types with one daily-life example for each. Name the physical quantity that measures inertia.",
                maxMarks: 3,
                questionType: "Short Definition",
                modelAnswer: "Inertia is the inherent property of an object by virtue of which it resists any change in its state of rest or of uniform motion in a straight line.\n\nThree Types:\n1. Inertia of Rest: A person jerks backward when a stationary bus starts suddenly.\n2. Inertia of Motion: A passenger falls forward when a moving bus brakes abruptly.\n3. Inertia of Direction: Water droplets flying off tangential to a rotating bicycle wheel.\n\nMeasurement: Mass is the quantitative measure of inertia of an object.",
                rubricPoints: [
                  "1.0 mark: Accurate scientific definition of inertia.",
                  "1.5 marks: Stating all 3 types (Rest, Motion, Direction) with correct daily-life examples.",
                  "0.5 mark: Explicitly stating that Mass is the measure of inertia."
                ]
              },
              {
                id: "q4",
                question: "A motorcar of mass 1200 kg is moving along a straight line with a uniform velocity of 90 km/h. Its velocity is slowed down to 18 km/h in 4 seconds by an unbalanced external force. Calculate the acceleration and the change in momentum. Also calculate the magnitude of the force required.",
                maxMarks: 5,
                questionType: "Derivation / Numerical",
                modelAnswer: "Given: Mass m = 1200 kg.\nInitial velocity u = 90 km/h = 90 * (5/18) = 25 m/s.\nFinal velocity v = 18 km/h = 18 * (5/18) = 5 m/s.\nTime t = 4 s.\n\n1. Acceleration:\na = (v - u) / t = (5 - 25) / 4 = -20 / 4 = -5 m/s² (Retardation).\n\n2. Change in Momentum:\nΔp = m(v - u) = 1200 * (5 - 25) = 1200 * (-20) = -24,000 kg·m/s.\n\n3. Force:\nF = m * a = 1200 * (-5) = -6000 N.\nMagnitude of force required = 6000 N (acting opposite to motion).",
                rubricPoints: [
                  "1.0 mark: Converting velocities from km/h to m/s correctly (u = 25 m/s, v = 5 m/s).",
                  "1.5 marks: Correct acceleration formula and calculation a = -5 m/s² with negative sign/retardation.",
                  "1.0 mark: Correct change in momentum Δp = -24,000 kg·m/s with units.",
                  "1.5 marks: Correct force magnitude F = 6000 N with correct SI unit (N)."
                ]
              },
              {
                id: "q5",
                question: "State Newton's Third Law of Motion. Why do action and reaction forces not cancel each other even though they are equal in magnitude and opposite in direction?",
                maxMarks: 4,
                questionType: "Conceptual Reasoning",
                modelAnswer: "Newton's Third Law of Motion states that to every action, there is an equal and opposite reaction.\n\nWhy they do not cancel:\nAction and reaction forces do not cancel each other because they ALWAYS ACT ON TWO DIFFERENT BODIES simultaneously, never on the same body.\nFor forces to cancel each other and produce zero net force, they must act on the same object. For example, when you walk on ground, your foot pushes the ground backward (Action on ground), and the ground pushes your foot forward (Reaction on foot). Because they act on different entities (ground and foot), motion is produced.",
                rubricPoints: [
                  "1.0 mark: Accurate statement of Newton's Third Law.",
                  "2.0 marks: Crucial reasoning that action and reaction act on TWO DIFFERENT BODIES simultaneously.",
                  "1.0 mark: Clear illustrative example (e.g., walking, swimming, rocket propulsion)."
                ]
              }
            ]
          },
          {
            id: "gravitation",
            title: "Gravitation and Floatation",
            ncertChapter: "NCERT Class 9 - Chapter 9",
            description: "Explore universal law of gravitation, free fall, mass vs weight, thrust & pressure, and Archimedes' principle.",
            concepts: [
              {
                id: "archimedes_buoyancy",
                name: "Archimedes' Principle & Floatation",
                summary: "When a body is immersed fully or partially in a fluid, it experiences an upward buoyant force equal to the weight of the fluid displaced by it.",
                teacherExplanation: "Have you ever tried pushing an inflated beach ball down into a bucket of water? You feel an upward push resisting you! That upward push is called Buoyant Force. Archimedes discovered that this buoyant force is exactly equal to the weight of water the ball pushes aside. If the buoyant force equals or exceeds the object's total weight, it floats! That's why a hollow steel ship floats while a tiny solid iron nail sinks.",
                audioScript: "Welcome to Gravitation and Floatation. Let's understand Archimedes' Principle. Any object placed in a liquid experiences an upward buoyant force. The magnitude of this force equals the weight of the displaced liquid. An iron nail sinks because solid iron is denser than water and displaces very little water. But an iron ship is built hollow with large volumes of trapped air. Its average density is far less than water, displacing an enormous volume of water whose weight easily balances the ship.",
                analogies: [
                  "Pushing a floating plastic mug upside down into a bucket of water.",
                  "Lifting a heavy stone under water feels lighter until it breaks the surface.",
                  "A swimmer feeling weightless in water."
                ],
                examples: [
                  {
                    title: "Example: Iron Nail vs Giant Cargo Ship",
                    scenario: "Both are made of iron. Why does the 5-gram nail sink while the 50,000-tonne ship floats?",
                    explanation: "The nail is solid with density ~7.8 g/cm³, displacing very little water. The ship is hollowed out; its total volume includes huge air compartments. Its average density (total mass / total volume) is less than water (1.0 g/cm³), allowing it to displace its own weight before submerging."
                  }
                ],
                keyFormulas: [
                  "Buoyant Force: F_b = V * ρ_fluid * g (Volume displaced * fluid density * g)",
                  "Pressure: P = Thrust / Area (SI unit: Pascal = N/m²)",
                  "Relative Density = Density of substance / Density of water (no unit)"
                ],
                commonMisconceptions: [
                  "Thinking buoyant force depends on the mass of the object rather than the volume of fluid displaced.",
                  "Confusing mass (constant, kg) with weight (gravitational pull, N)."
                ],
                authenticReferences: [
                  {
                    title: "NCERT Chapter 9: Floatation and Archimedes' Principle",
                    url: "https://ncert.nic.in/textbook.php?iesc1=9-15",
                    source: "NCERT"
                  },
                  {
                    title: "Khan Academy: Buoyant force and Archimedes' Principle",
                    url: "https://www.khanacademy.org/science/physics/fluids",
                    source: "Khan Academy"
                  }
                ]
              }
            ],
            practiceExamples: [],
            subjectivePaper: []
          }
        ]
      },
      {
        id: "chemistry",
        name: "Chemistry",
        icon: "FlaskConical",
        accentColor: "from-emerald-600 to-teal-700",
        chapters: [
          {
            id: "matter_surroundings",
            title: "Matter in Our Surroundings",
            ncertChapter: "NCERT Class 9 - Chapter 1",
            description: "Physical nature of matter, characteristics of particles, states of matter, and evaporation.",
            concepts: [
              {
                id: "evaporation_cooling",
                name: "Evaporation & Factors Affecting Cooling",
                summary: "Evaporation is a surface phenomenon where liquid turns to vapor at temperatures below boiling point, causing cooling.",
                teacherExplanation: "When you pour a few drops of acetone or perfume on your palm, your hand feels cold. Why? The liquid particles take heat energy from your palm to evaporate, leaving your hand cooler!",
                audioScript: "Let's study Evaporation in Class 9 Chemistry. Evaporation is a surface phenomenon. Particles at the surface gain kinetic energy from surroundings and escape into vapor. This absorption of latent heat causes cooling.",
                analogies: [
                  "Earthen pots (matka) keeping water cool in Indian summers.",
                  "Wearing cotton clothes in summer to absorb sweat and promote cooling.",
                  "Spreading clothes wide on a line to increase surface area for faster drying."
                ],
                examples: [
                  {
                    title: "Example: Why wear cotton clothes in summer?",
                    scenario: "During summer, our body perspires heavily to regulate temperature.",
                    explanation: "Cotton is a good absorber of water. It absorbs sweat and exposes it to the atmosphere for easy evaporation. The heat energy equal to latent heat of vaporization is absorbed from body, cooling us."
                  }
                ],
                keyFormulas: [
                  "Rate of evaporation ∝ Surface Area",
                  "Rate of evaporation ∝ Temperature",
                  "Rate of evaporation ∝ Wind Speed",
                  "Rate of evaporation ∝ 1 / Humidity"
                ],
                commonMisconceptions: [
                  "Confusing evaporation (occurs at any temp below boiling point) with boiling (bulk phenomenon at specific boiling point)."
                ],
                authenticReferences: [
                  {
                    title: "NCERT Class 9 Chemistry - Matter in Our Surroundings",
                    url: "https://ncert.nic.in/textbook.php?iesc1=1-15",
                    source: "NCERT"
                  }
                ]
              }
            ],
            practiceExamples: [],
            subjectivePaper: []
          }
        ]
      },
      {
        id: "biology",
        name: "Biology",
        icon: "Dna",
        accentColor: "from-green-600 to-emerald-800",
        chapters: [
          {
            id: "cell_fundamental_unit",
            title: "The Fundamental Unit of Life (Cell)",
            ncertChapter: "NCERT Class 9 - Chapter 5",
            description: "Cell structure, plasma membrane, nucleus, cytoplasm, and cell organelles.",
            concepts: [
              {
                id: "osmosis_plasmolysis",
                name: "Osmosis, Diffusion & Cell Membrane",
                summary: "Osmosis is the passage of water from a region of high water concentration through a selectively permeable membrane to low water concentration.",
                teacherExplanation: "Think of raisins placed in water overnight. They swell up because water enters inside them through osmosis!",
                audioScript: "Cell biology begins with the plasma membrane. It is selectively permeable. Osmosis is the diffusion of water molecules across this membrane. In hypotonic solutions, cells swell; in hypertonic, they shrink.",
                analogies: [
                  "Dried raisins swelling in a bowl of pure water.",
                  "Salt sprinkled on raw salad causing cucumber to release water."
                ],
                examples: [
                  {
                    title: "Example: Swelling of Raisins",
                    scenario: "Dry kishmish placed in plain water for 3 hours.",
                    explanation: "Surrounding water has higher concentration than inside the raisin cell sap. Endosmosis occurs and raisins swell."
                  }
                ],
                keyFormulas: [
                  "Hypotonic: External water concentration > Cell -> Endosmosis (Swells)",
                  "Hypertonic: External water concentration < Cell -> Exosmosis (Shrinks)",
                  "Isotonic: Same concentration -> No net movement"
                ],
                commonMisconceptions: [
                  "Confusing diffusion (any substance, no membrane required) with osmosis (water through selectively permeable membrane)."
                ],
                authenticReferences: [
                  {
                    title: "NCERT Class 9 Biology - The Fundamental Unit of Life",
                    url: "https://ncert.nic.in/textbook.php?iesc1=5-15",
                    source: "NCERT"
                  }
                ]
              }
            ],
            practiceExamples: [],
            subjectivePaper: []
          }
        ]
      },
      {
        id: "mathematics",
        name: "Mathematics",
        icon: "Calculator",
        accentColor: "from-purple-600 to-violet-800",
        chapters: [
          {
            id: "number_systems",
            title: "Number Systems",
            ncertChapter: "NCERT Class 9 - Chapter 1",
            description: "Rational & irrational numbers, real numbers and decimal expansions, laws of exponents.",
            concepts: [
              {
                id: "irrational_proofs",
                name: "Rational vs Irrational Numbers",
                summary: "A number is irrational if its decimal expansion is non-terminating and non-recurring (e.g., √2, π).",
                teacherExplanation: "Rational numbers can be written as p/q where q is not zero. But irrational numbers cannot be expressed as a fraction; their decimals go on forever without any repeating pattern!",
                audioScript: "In Class 9 Mathematics, rational numbers like 1/2 or 0.333 recurring can be written as p over q. But numbers like the square root of 2 or pi are irrational because their decimal expansion never ends and never repeats.",
                analogies: [
                  "Walking along a grid vs measuring the exact hypotenuse diagonal."
                ],
                examples: [
                  {
                    title: "Example: Representing √2 on number line",
                    scenario: "Construct a right triangle with base = 1 unit, height = 1 unit.",
                    explanation: "By Pythagoras theorem, hypotenuse = √(1² + 1²) = √2. An arc drawn with compass marks √2 on the line."
                  }
                ],
                keyFormulas: [
                  "Pythagoras: c = √(a² + b²)",
                  "Laws of Exponents: a^m * a^n = a^(m+n)"
                ],
                commonMisconceptions: [
                  "Assuming 22/7 is equal to π; 22/7 is an approximate rational fraction, whereas π is strictly irrational."
                ],
                authenticReferences: [
                  {
                    title: "NCERT Class 9 Maths - Number Systems",
                    url: "https://ncert.nic.in/textbook.php?iemh1=1-15",
                    source: "NCERT"
                  }
                ]
              }
            ],
            practiceExamples: [],
            subjectivePaper: []
          }
        ]
      }
    ]
  },
  8: {
    className: "Class 8th (Middle School)",
    classNumber: 8,
    subjects: [
      {
        id: "physics_8",
        name: "Science (Physics Foundations)",
        icon: "Atom",
        accentColor: "from-sky-600 to-blue-700",
        chapters: [
          {
            id: "force_pressure_8",
            title: "Force and Pressure",
            ncertChapter: "NCERT Class 8 - Chapter 8",
            description: "Introduction to push and pull, contact and non-contact forces, atmospheric pressure.",
            concepts: [
              {
                id: "force_types",
                name: "Contact and Non-Contact Forces",
                summary: "Forces requiring physical contact (muscular, friction) versus forces acting from a distance (gravitational, magnetic, electrostatic).",
                teacherExplanation: "Whenever you kick a ball, your foot touches it (contact force). But when a magnet pulls an iron nail, it happens across empty air (non-contact force)!",
                audioScript: "In Class 8 Science, forces are classified as contact and non-contact. Muscular and frictional forces require physical touch, while magnetic, electrostatic, and gravitational forces act at a distance.",
                analogies: ["Kicking a football vs a magnet picking up paper clips."],
                examples: [],
                keyFormulas: ["Pressure = Force / Area"],
                commonMisconceptions: ["Assuming friction only opposes motion and has no useful purpose."],
                authenticReferences: [{ title: "NCERT Class 8 Science", url: "https://ncert.nic.in", source: "NCERT" }]
              }
            ],
            practiceExamples: [],
            subjectivePaper: []
          }
        ]
      }
    ]
  },
  10: {
    className: "Class 10th (Secondary Board Exam)",
    classNumber: 10,
    subjects: [
      {
        id: "physics_10",
        name: "Physics",
        icon: "Zap",
        accentColor: "from-amber-600 to-orange-700",
        chapters: [
          {
            id: "light_reflection",
            title: "Light: Reflection and Refraction",
            ncertChapter: "NCERT Class 10 - Chapter 9",
            description: "Spherical mirrors, mirror formula, Snell's law, refractive index, and lens formula.",
            concepts: [
              {
                id: "snell_law",
                name: "Snell's Law of Refraction",
                summary: "The ratio of the sine of the angle of incidence to the sine of the angle of refraction is a constant for a given pair of media.",
                teacherExplanation: "When light travels from air into water, it bends towards the normal. Snell's law gives us the exact mathematical formula: sin i / sin r = constant (refractive index n).",
                audioScript: "Welcome to Class 10 Physics. Snell's law tells us how light bends when crossing optical boundaries. The ratio of sine of incidence angle to sine of refraction angle equals the relative refractive index of the medium.",
                analogies: ["A shopping cart hitting a patch of grass diagonally and pivoting."],
                examples: [],
                keyFormulas: ["sin i / sin r = n2 / n1", "Mirror Formula: 1/f = 1/v + 1/u"],
                commonMisconceptions: ["Measuring angles from the surface instead of measuring from the normal line."],
                authenticReferences: [{ title: "NCERT Class 10 Physics", url: "https://ncert.nic.in", source: "NCERT" }]
              }
            ],
            practiceExamples: [],
            subjectivePaper: []
          }
        ]
      }
    ]
  }
};

export const AVAILABLE_BOARDS = [
  { id: "cbse", name: "CBSE (All India)", badge: "Central Board", color: "bg-blue-100 text-blue-800 border-blue-300" },
  { id: "icse", name: "ICSE / CISCE", badge: "Council Board", color: "bg-purple-100 text-purple-800 border-purple-300" },
  { id: "state_board", name: "State Board (Maharashtra / UP / Karnataka / etc.)", badge: "State Syllabus", color: "bg-emerald-100 text-emerald-800 border-emerald-300" },
  { id: "cambridge", name: "Cambridge IGCSE", badge: "International", color: "bg-amber-100 text-amber-800 border-amber-300" }
];
