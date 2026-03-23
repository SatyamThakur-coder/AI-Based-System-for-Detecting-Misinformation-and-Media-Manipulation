"""
Comprehensive seed knowledge base for fact-checking
Covers: anatomy, science, technology, history, geography, math, space,
        health, politics, economics, environment, and common myths
"""

SEED_KNOWLEDGE = [
    # =========================================================================
    # HUMAN ANATOMY & BIOLOGY
    # =========================================================================
    {"text": "Humans typically have 2 hands, 2 legs, 2 eyes, 2 ears, 1 nose, and 1 mouth.", "source": "Anatomy Basics", "url": "https://www.britannica.com/science/human-body", "category": "biology", "verified": True},
    {"text": "The human body has 206 bones in adults and approximately 270 bones at birth, some of which fuse together during development.", "source": "NIH", "url": "https://www.ncbi.nlm.nih.gov/books/NBK45504/", "category": "biology", "verified": True},
    {"text": "The human heart beats approximately 100,000 times per day and pumps about 2,000 gallons of blood.", "source": "American Heart Association", "url": "https://www.heart.org/", "category": "biology", "verified": True},
    {"text": "Human DNA is approximately 99.9% identical between any two people on Earth.", "source": "NIH Genome", "url": "https://www.genome.gov/", "category": "biology", "verified": True},
    {"text": "The human brain contains approximately 86 billion neurons connected by trillions of synapses.", "source": "Nature Neuroscience", "url": "https://www.nature.com/neuro/", "category": "biology", "verified": True},
    {"text": "Human blood is composed of red blood cells, white blood cells, platelets, and plasma.", "source": "American Red Cross", "url": "https://www.redcross.org/", "category": "biology", "verified": True},
    {"text": "Humans have 5 basic senses: sight, hearing, smell, taste, and touch.", "source": "Encyclopedia Britannica", "url": "https://www.britannica.com/science/human-sensory-reception", "category": "biology", "verified": True},
    {"text": "The average adult human body is about 60% water by weight.", "source": "USGS", "url": "https://www.usgs.gov/special-topics/water-science-school", "category": "biology", "verified": True},
    {"text": "Humans have 32 permanent teeth as adults and 20 primary (baby) teeth as children.", "source": "ADA", "url": "https://www.ada.org/", "category": "biology", "verified": True},
    {"text": "The human eye can distinguish approximately 10 million different colors.", "source": "American Academy of Ophthalmology", "url": "https://www.aao.org/", "category": "biology", "verified": True},

    # =========================================================================
    # EARTH SCIENCE & GEOGRAPHY
    # =========================================================================
    {"text": "The Earth is approximately 4.5 billion years old based on radiometric dating of rocks and meteorites.", "source": "USGS", "url": "https://www.usgs.gov/faqs/how-old-earth", "category": "science", "verified": True},
    {"text": "The Earth is roughly spherical (an oblate spheroid) and orbits the Sun at an average distance of about 93 million miles.", "source": "NASA", "url": "https://science.nasa.gov/earth/facts/", "category": "science", "verified": True},
    {"text": "Earth has 7 continents: Africa, Antarctica, Asia, Australia, Europe, North America, and South America.", "source": "National Geographic", "url": "https://www.nationalgeographic.org/", "category": "geography", "verified": True},
    {"text": "Earth has 5 major oceans: Pacific, Atlantic, Indian, Southern (Antarctic), and Arctic.", "source": "NOAA", "url": "https://www.noaa.gov/", "category": "geography", "verified": True},
    {"text": "Mount Everest is the tallest mountain above sea level at approximately 8,849 meters (29,032 feet).", "source": "National Geographic", "url": "https://www.nationalgeographic.com/environment/article/mount-everest", "category": "geography", "verified": True},
    {"text": "The Mariana Trench is the deepest point in the ocean at approximately 10,994 meters (36,070 feet) deep.", "source": "NOAA", "url": "https://oceanexplorer.noaa.gov/", "category": "geography", "verified": True},
    {"text": "The Sahara is the largest hot desert in the world, covering approximately 9.2 million square kilometers in northern Africa.", "source": "Britannica", "url": "https://www.britannica.com/place/Sahara-desert-Africa", "category": "geography", "verified": True},
    {"text": "The Nile River and the Amazon River are among the longest rivers in the world, each approximately 6,650 km and 6,400 km respectively.", "source": "Encyclopedia Britannica", "url": "https://www.britannica.com/", "category": "geography", "verified": True},
    {"text": "Russia is the largest country in the world by area, spanning over 17.1 million square kilometers.", "source": "CIA World Factbook", "url": "https://www.cia.gov/the-world-factbook/", "category": "geography", "verified": True},
    {"text": "India has a population of approximately 1.4 billion people and China has approximately 1.4 billion people, making them the two most populous countries.", "source": "United Nations", "url": "https://www.un.org/", "category": "geography", "verified": True},

    # =========================================================================
    # PHYSICS & CHEMISTRY
    # =========================================================================
    {"text": "Water is composed of two hydrogen atoms and one oxygen atom (H2O).", "source": "Chemistry Fundamentals", "url": "https://www.britannica.com/science/water", "category": "science", "verified": True},
    {"text": "The speed of light in a vacuum is approximately 299,792,458 meters per second.", "source": "NIST", "url": "https://www.nist.gov/si-redefinition/meter", "category": "science", "verified": True},
    {"text": "Gravity is the force of attraction between objects with mass. On Earth, gravitational acceleration is approximately 9.8 m/s².", "source": "NASA", "url": "https://science.nasa.gov/", "category": "science", "verified": True},
    {"text": "An atom is composed of protons, neutrons, and electrons. Protons and neutrons form the nucleus.", "source": "CERN", "url": "https://home.cern/", "category": "science", "verified": True},
    {"text": "Einstein's equation E=mc² shows that energy and mass are interchangeable, where c is the speed of light.", "source": "American Physical Society", "url": "https://www.aps.org/", "category": "science", "verified": True},
    {"text": "The periodic table organizes chemical elements by atomic number. There are currently 118 confirmed elements.", "source": "IUPAC", "url": "https://iupac.org/", "category": "science", "verified": True},
    {"text": "Water freezes at 0 degrees Celsius (32°F) and boils at 100 degrees Celsius (212°F) at standard atmospheric pressure.", "source": "Physics Fundamentals", "url": "https://www.britannica.com/science/water", "category": "science", "verified": True},
    {"text": "Sound travels at approximately 343 meters per second in air at room temperature.", "source": "Physics Today", "url": "https://physicstoday.scitation.org/", "category": "science", "verified": True},

    # =========================================================================
    # SPACE & ASTRONOMY
    # =========================================================================
    {"text": "The Sun is a medium-sized star approximately 4.6 billion years old and is about 93 million miles from Earth.", "source": "NASA", "url": "https://science.nasa.gov/sun/", "category": "space", "verified": True},
    {"text": "The Moon orbits the Earth at an average distance of about 384,400 km and causes ocean tides through gravitational pull.", "source": "NASA", "url": "https://moon.nasa.gov/", "category": "space", "verified": True},
    {"text": "Our solar system has 8 planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Pluto was reclassified as a dwarf planet in 2006.", "source": "NASA", "url": "https://science.nasa.gov/solar-system/", "category": "space", "verified": True},
    {"text": "Jupiter is the largest planet in our solar system, with a mass more than twice that of all other planets combined.", "source": "NASA", "url": "https://science.nasa.gov/jupiter/", "category": "space", "verified": True},
    {"text": "The Milky Way galaxy contains an estimated 100 to 400 billion stars and is approximately 100,000 light-years in diameter.", "source": "ESA", "url": "https://www.esa.int/", "category": "space", "verified": True},
    {"text": "Light from the Sun takes approximately 8 minutes and 20 seconds to reach Earth.", "source": "NASA", "url": "https://science.nasa.gov/", "category": "space", "verified": True},
    {"text": "Neil Armstrong became the first human to walk on the Moon on July 20, 1969, during the Apollo 11 mission.", "source": "NASA", "url": "https://www.nasa.gov/mission_pages/apollo/apollo11.html", "category": "history", "verified": True},
    {"text": "Mars is known as the Red Planet due to iron oxide (rust) on its surface and has a thin atmosphere mostly of carbon dioxide.", "source": "NASA", "url": "https://science.nasa.gov/mars/", "category": "space", "verified": True},

    # =========================================================================
    # HISTORY
    # =========================================================================
    {"text": "World War II lasted from 1939 to 1945 and involved most of the world's nations.", "source": "History.com", "url": "https://www.history.com/topics/world-war-ii", "category": "history", "verified": True},
    {"text": "World War I lasted from 1914 to 1918 and was triggered in part by the assassination of Archduke Franz Ferdinand.", "source": "History.com", "url": "https://www.history.com/topics/world-war-i", "category": "history", "verified": True},
    {"text": "The Declaration of Independence of the United States was adopted on July 4, 1776.", "source": "National Archives", "url": "https://www.archives.gov/founding-docs/declaration", "category": "history", "verified": True},
    {"text": "India gained independence from British rule on August 15, 1947. Mahatma Gandhi was a key leader in the independence movement.", "source": "Government of India", "url": "https://www.india.gov.in/", "category": "history", "verified": True},
    {"text": "The Berlin Wall fell on November 9, 1989, marking a pivotal moment in the end of the Cold War.", "source": "BBC History", "url": "https://www.bbc.co.uk/history/", "category": "history", "verified": True},
    {"text": "The Great Wall of China was built over many centuries, primarily during the Ming Dynasty (1368-1644), and stretches approximately 21,196 km.", "source": "UNESCO", "url": "https://whc.unesco.org/", "category": "history", "verified": True},
    {"text": "The ancient Egyptian pyramids of Giza were built approximately 4,500 years ago as tombs for pharaohs.", "source": "National Geographic", "url": "https://www.nationalgeographic.com/history/article/giza-pyramids", "category": "history", "verified": True},
    {"text": "The Renaissance was a cultural movement that began in Italy around the 14th century and spread across Europe.", "source": "Britannica", "url": "https://www.britannica.com/event/Renaissance", "category": "history", "verified": True},
    {"text": "The French Revolution began in 1789 with the storming of the Bastille and led to major political changes in France.", "source": "History.com", "url": "https://www.history.com/topics/france/french-revolution", "category": "history", "verified": True},

    # =========================================================================
    # TECHNOLOGY
    # =========================================================================
    {"text": "The internet was developed from ARPANET, a project funded by the U.S. Department of Defense, in the late 1960s.", "source": "Computer History Museum", "url": "https://www.computerhistory.org/", "category": "technology", "verified": True},
    {"text": "Tim Berners-Lee invented the World Wide Web in 1989 while working at CERN.", "source": "CERN", "url": "https://home.cern/science/computing/birth-web", "category": "technology", "verified": True},
    {"text": "Artificial intelligence is the simulation of human intelligence by computer systems, including learning, reasoning, and self-correction.", "source": "MIT Technology Review", "url": "https://www.technologyreview.com/", "category": "technology", "verified": True},
    {"text": "Moore's Law observes that the number of transistors on a microchip roughly doubles every two years.", "source": "Intel", "url": "https://www.intel.com/", "category": "technology", "verified": True},
    {"text": "The first programmable electronic computer, ENIAC, was completed in 1945 at the University of Pennsylvania.", "source": "Computer History Museum", "url": "https://www.computerhistory.org/", "category": "technology", "verified": True},
    {"text": "Bitcoin, the first decentralized cryptocurrency, was created in 2009 by an anonymous entity known as Satoshi Nakamoto.", "source": "Bitcoin.org", "url": "https://bitcoin.org/", "category": "technology", "verified": True},
    {"text": "5G is the fifth generation of wireless technology, offering faster speeds and lower latency than 4G networks.", "source": "IEEE", "url": "https://www.ieee.org/", "category": "technology", "verified": True},

    # =========================================================================
    # HEALTH & MEDICINE
    # =========================================================================
    {"text": "COVID-19 vaccines have been proven safe and effective through extensive clinical trials involving tens of thousands of participants.", "source": "WHO", "url": "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/covid-19-vaccines", "category": "health", "verified": True},
    {"text": "Antibiotics treat bacterial infections but are ineffective against viruses such as the common cold or flu.", "source": "CDC", "url": "https://www.cdc.gov/antibiotic-use/", "category": "health", "verified": True},
    {"text": "Vaccines work by training the immune system to recognize and fight specific pathogens without causing the disease.", "source": "WHO", "url": "https://www.who.int/news-room/feature-stories/detail/how-do-vaccines-work", "category": "health", "verified": True},
    {"text": "Regular physical exercise reduces the risk of heart disease, diabetes, depression, and many types of cancer.", "source": "WHO", "url": "https://www.who.int/news-room/fact-sheets/detail/physical-activity", "category": "health", "verified": True},
    {"text": "Smoking tobacco is the leading cause of preventable death worldwide, causing cancer, heart disease, and lung disease.", "source": "WHO", "url": "https://www.who.int/news-room/fact-sheets/detail/tobacco", "category": "health", "verified": True},
    {"text": "Penicillin, the first widely used antibiotic, was discovered by Alexander Fleming in 1928.", "source": "Nobel Prize", "url": "https://www.nobelprize.org/prizes/medicine/1945/fleming/biographical/", "category": "health", "verified": True},
    {"text": "The human body has about 5 liters of blood and the heart pumps all of it through the body every minute at rest.", "source": "NIH", "url": "https://www.nih.gov/", "category": "health", "verified": True},

    # =========================================================================
    # CLIMATE & ENVIRONMENT
    # =========================================================================
    {"text": "Climate change is supported by over 97% of climate scientists according to peer-reviewed research.", "source": "NASA Climate", "url": "https://climate.nasa.gov/scientific-consensus/", "category": "science", "verified": True},
    {"text": "The global average temperature has risen by approximately 1.1°C since the pre-industrial era, primarily due to human activities.", "source": "IPCC", "url": "https://www.ipcc.ch/", "category": "science", "verified": True},
    {"text": "Deforestation contributes to climate change by reducing the number of trees that absorb carbon dioxide.", "source": "WWF", "url": "https://www.worldwildlife.org/threats/deforestation-and-forest-degradation", "category": "environment", "verified": True},
    {"text": "The ozone layer protects Earth from harmful ultraviolet radiation. The Montreal Protocol of 1987 banned ozone-depleting substances.", "source": "UNEP", "url": "https://www.unep.org/ozonaction/", "category": "environment", "verified": True},
    {"text": "Renewable energy sources include solar, wind, hydroelectric, geothermal, and biomass.", "source": "IEA", "url": "https://www.iea.org/", "category": "environment", "verified": True},

    # =========================================================================
    # MATHEMATICS
    # =========================================================================
    {"text": "Pi (π) is approximately 3.14159 and represents the ratio of a circle's circumference to its diameter.", "source": "Mathematics", "url": "https://www.britannica.com/science/pi-mathematics", "category": "math", "verified": True},
    {"text": "The Pythagorean theorem states that in a right triangle, a² + b² = c², where c is the hypotenuse.", "source": "Mathematics", "url": "https://www.britannica.com/science/Pythagorean-theorem", "category": "math", "verified": True},
    {"text": "Zero was first used as a number by ancient Indian mathematicians around the 5th century CE.", "source": "Mathematics History", "url": "https://www.britannica.com/science/zero-mathematics", "category": "math", "verified": True},
    {"text": "A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.", "source": "Mathematics", "url": "https://www.britannica.com/science/prime-number", "category": "math", "verified": True},
    {"text": "2 + 2 = 4. Basic arithmetic operations include addition, subtraction, multiplication, and division.", "source": "Mathematics", "url": "https://www.britannica.com/science/arithmetic", "category": "math", "verified": True},

    # =========================================================================
    # ANIMALS & NATURE
    # =========================================================================
    {"text": "The blue whale is the largest animal ever known to have lived on Earth, reaching lengths of up to 30 meters (100 feet).", "source": "National Geographic", "url": "https://www.nationalgeographic.com/animals/mammals/facts/blue-whale", "category": "biology", "verified": True},
    {"text": "Dogs were domesticated from wolves approximately 15,000 to 40,000 years ago.", "source": "Smithsonian", "url": "https://www.si.edu/", "category": "biology", "verified": True},
    {"text": "Photosynthesis is the process by which green plants convert sunlight, water, and carbon dioxide into glucose and oxygen.", "source": "Biology", "url": "https://www.britannica.com/science/photosynthesis", "category": "biology", "verified": True},
    {"text": "Dinosaurs went extinct approximately 66 million years ago, likely due to an asteroid impact.", "source": "Smithsonian", "url": "https://www.si.edu/", "category": "biology", "verified": True},
    {"text": "Cats have excellent night vision and can see in light levels six times lower than what humans need.", "source": "Veterinary Science", "url": "https://www.avma.org/", "category": "biology", "verified": True},
    {"text": "The cheetah is the fastest land animal, capable of reaching speeds up to 120 km/h (75 mph) in short bursts.", "source": "National Geographic", "url": "https://www.nationalgeographic.com/", "category": "biology", "verified": True},

    # =========================================================================
    # COMMON MYTHS & MISINFORMATION
    # =========================================================================
    {"text": "The Earth is not flat. It is an oblate spheroid (slightly flattened at the poles), confirmed by centuries of scientific evidence, satellite imagery, and space exploration.", "source": "NASA", "url": "https://science.nasa.gov/earth/facts/", "category": "myth_debunk", "verified": True},
    {"text": "5G technology does not cause COVID-19 or other diseases. Radio waves used by 5G are non-ionizing and cannot create or spread viruses.", "source": "WHO", "url": "https://www.who.int/", "category": "myth_debunk", "verified": True},
    {"text": "Vaccines do not cause autism. This claim originated from a fraudulent 1998 study that was retracted and its author lost his medical license.", "source": "CDC", "url": "https://www.cdc.gov/vaccinesafety/concerns/autism.html", "category": "myth_debunk", "verified": True},
    {"text": "Humans use all parts of their brain, not just 10%. Brain imaging studies show activity throughout the entire brain.", "source": "Scientific American", "url": "https://www.scientificamerican.com/", "category": "myth_debunk", "verified": True},
    {"text": "COVID-19 vaccines do not contain microchips. Vaccines contain mRNA or viral proteins, lipids, salts, and sugars.", "source": "CDC", "url": "https://www.cdc.gov/vaccines/covid-19/", "category": "myth_debunk", "verified": True},
    {"text": "The Great Wall of China is not visible from space with the naked eye. This is a common misconception.", "source": "NASA", "url": "https://www.nasa.gov/", "category": "myth_debunk", "verified": True},
    {"text": "Lightning can and does strike the same place twice. Tall structures like the Empire State Building are struck dozens of times per year.", "source": "NOAA", "url": "https://www.weather.gov/safety/lightning-myths", "category": "myth_debunk", "verified": True},

    # =========================================================================
    # ECONOMICS & POLITICS
    # =========================================================================
    {"text": "The United Nations was founded in 1945 after World War II with the goal of maintaining international peace and security.", "source": "United Nations", "url": "https://www.un.org/en/about-us", "category": "politics", "verified": True},
    {"text": "Democracy is a system of government where power is vested in the people, who exercise it through elected representatives.", "source": "Britannica", "url": "https://www.britannica.com/topic/democracy", "category": "politics", "verified": True},
    {"text": "GDP (Gross Domestic Product) measures the total value of goods and services produced in a country over a specific period.", "source": "World Bank", "url": "https://www.worldbank.org/", "category": "economics", "verified": True},
    {"text": "Inflation is the rate at which the general level of prices for goods and services rises, reducing purchasing power.", "source": "Federal Reserve", "url": "https://www.federalreserve.gov/", "category": "economics", "verified": True},

    # =========================================================================
    # CULTURE & LANGUAGE
    # =========================================================================
    {"text": "Mandarin Chinese is the most spoken language in the world by total number of speakers, followed by Spanish and English.", "source": "Ethnologue", "url": "https://www.ethnologue.com/", "category": "culture", "verified": True},
    {"text": "The Olympic Games originated in ancient Greece around 776 BC and were revived in 1896 as the modern Olympics.", "source": "IOC", "url": "https://olympics.com/", "category": "culture", "verified": True},
    {"text": "Shakespeare wrote approximately 37 plays and 154 sonnets and is widely regarded as the greatest writer in the English language.", "source": "Britannica", "url": "https://www.britannica.com/biography/William-Shakespeare", "category": "culture", "verified": True},
]
