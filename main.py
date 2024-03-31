import streamlit as st
import re
import speech_recognition as sr
from nltk.chat.util import reflections
from gtts import gTTS
import tempfile
import moviepy.editor as mp
import base64

pairs = [
    (r"(hello|hi|hey|start)", ["Hello! i am Lanturn! ", "Hi there!"]),
    (r"(.*)(check water quality|ways to check water)(.*)", [
        "If the water is clear and has no visible particles, it is a good sign."
        "Cloudy water or water with particles may contain impurities."
    ]),
    (r"(.*)(report)(.*)", [
        "Contact Details:\nCentral Pollution Control Board Postal Address: Parivesh Bhawan, East Arjun Nagar, Delhi-110032\nEPABX No.: +91-11-43102030\nE-mail: ccb.cpcb@nic.in"
    ]),
    (r"(.*)(pollution sources in rivers|sources)(.*)", [
        "River pollution sources include:\n- Industrial Waste\n- Marine Dumping\n- Sewage and Wastewater"
        "- Oil Leaks and Spills\n- Agriculture\n- Global Warming\n- Radioactive Waste"
    ]),
    (r"(.*)(reduce water pollution|stop water pollution)(.*)", [
        "- Monitor and Regulate Pollution Sources"
        "- Educate and Raise Awareness\n- Support Wastewater Treatment\n- Reduce Thermal Pollution\n- Support Legislation and Regulations"
        "- Participate in Cleanup Efforts\n- Properly Dispose of Household Hazardous Waste\n- Minimize Chemical Usage"
        "- Control Erosion\n- Properly Manage Stormwater\n- Maintain Your Vehicle\n- Reduce Plastic Waste\n- Upgrade and Maintain Septic Systems"
        "- Promote Sustainable Agriculture\n- Implement Industrial Best Practices"
    ]),
    (r"(.*)(government|authorities | govt)(.*)", [
        "\n- Central Pollution Control Board (CPCB)"
        "- State Pollution Control Boards (SPCBs)\n- Pollution Control Committees (PCCs)\n- Central Water Commission (CWC), you can team up with them to help save a waterbody near you"        
    ]),
    (r"(.*)(ngos|volunteer)(.*)", [
        "Organizations for river cleanup and volunteering:\n- Water.org\n- WaterAid\n- World Wildlife Fund (WWF)"
        "- Charity: Water\n- The Nature Conservancy\n- UNICEF Water, Sanitation, and Hygiene (WASH) Program\n- Water For People"
    ]),
    (r"(.*)(water body initiatives|programs)(.*)", [
        "Recent initiatives for water body cleanliness:\n- Namami Gange\n- Swachh Bharat Mission (SBM)\n- Amrit Sarovar Mission"
        "- River Rejuvenation Program\n- Clean Lake Program\n- Catch the Rain\n- Jal Jeevan Mission"
    ]),
    (r"(.*)(daily practices)(.*)", [
        " \n- Reduce the use of pesticides, herbicides, and fertilizers"
        "- Pick up after your pet\n- Wash your car less often\n- Dispose of hazardous waste properly"
        "- Conserve water\n- Use eco-friendly cleaning products\n- Avoid single-use plastics\n- Support sustainable businesses"
    ]),
    (r"(.*)(health risks | health hazards)(.*)", [
        "\n- Gastrointestinal illnesses"
        "- Skin infections\n- Respiratory infections"
    ]),
    (r"(.*)(pollution regulations | laws | acts)(.*)", [
        "Regulations and policies to protect water bodies:\n- The Water (Prevention and Control of Pollution) Act, 1974"
        "- The Environment (Protection) Act, 1986\n- The Water (Prevention and Control of Pollution) Cess Act, 1977"
        "- The Indian Penal Code, 1860 (Section 277)\n- State water pollution laws (e.g., Maharashtra Water (Prevention and Control of Pollution) Act, 1974, and Tamil Nadu Water (Prevention and Control of Pollution) Act, 1974)"
    ]),
    (r"(.*)(common water pollutants | common pollutants | common things that pollute water)(.*)", [
        "Common water pollutants include:\n- Cleaning products like bleach and liquid detergent"
        "- Personal hygiene products like lotions and cosmetics\n- Certain medications\n- Pesticides and insecticides used in farming"
        "- Paints, solvents, and thinners\n- Motor oils like petrol and diesel\n- Plastic bags and microplastics\n- E-waste"
    ]),
    (r"(.*)(cleanup project funding | money)(.*)", [
        "Funding opportunities for water body cleanup projects:\n- National River Conservation Plan"
        "- Clean Ganga Fund (nmcg.nic.in)\n- Corporate social responsibility\n- Arghyam\n- Vasundhara foundation"
        "- Waste warriors\n- Environmentalist foundation of India\n- Goonj\n- River connect campaign"
    ]),
    (r"(.*)(detect local water pollution  | how to tell if water is polluted)(.*)", [
        "Signs of polluted local water bodies:\n- Unusual odor\n- Presence of scum\n- Unusual behavior of aquatic animals"
        "- Excessive growth of algae\n- Presence of plastic, litter, etc.\n- Discolored water"
    ]),
    (r"(.*)(aquatic ecosystem impact | marine life | aquatic life)(.*)", [
        "Impact of pollution on aquatic ecosystems and wildlife:\n- Loss of biodiversity\n- Habitat destruction"
        "- Poisoning of water bodies\n- Disruption of the food chain\n- Reduced economic value"
    ]),
    (r"(.*)(not to do near water bodies | things to avoid)(.*)", [
        "Eco-friendly practices near water bodies:\n1. Don't submerge anything with chemical content into water"
        "2. Don't dispose trash into water bodies\n3. Avoid damaging aquatic habitat"
    ]),
    (r"(.*)(cleanliness drive alerts | drive alerts | campaign alerts)(.*)", [
        "Websites to receive alerts for cleanliness drives:\n- https://www.mygov.in\n- https://swechha.in"
    ]),
    (r"(.*)(reduce household water usage|save water)(.*)", [
        "Ways to reduce household water usage:\n- Fix any leaks in your plumbing"
        "- Take shorter showers\n- Turn off the faucet when you brush your teeth or shave\n- Water your lawn less often"
        "- Install water-efficient appliances"
    ]),
    (r"(.*)(agricultural runoff impact | agriculture practices)(.*)", [
        "Impact of agricultural runoff on water bodies:\n- Algae blooms\n- Eutrophication\n- Harm to aquatic life"
    ]),
    (r"(.*)(urban water pollutants | water pollutants in cities)(.*)", [
        "Common water pollutants in urban areas:\n- Oil and grease\n- Heavy metals\n- Pesticides"
        "- Fertilizers\n- Bacteria and viruses\n- Sediment\n- Trash"
    ]),
    (r"(.*)(wetlands importance)(.*)", [
        "Importance of wetlands in water body protection:\n- Natural filters",
        "- Removing pollutants from water\n- Providing habitat for fish, birds, and other wildlife"
        "- Helping to reduce flooding and erosion"
    ]),
    (r"(.*)(prevent lake eutrophication)(.*)", [
        "Measures to prevent lake eutrophication:\n- Reduce the amount of nutrients entering the lake",
        "- Divert stormwater runoff away from the lake\n- Plant trees and other vegetation around the lake to help filter runoff"
    ]),
    (r"(.*)(dispose cleaning chemicals)(.*)", [
        "Safe disposal of old household cleaning chemicals:\n- Take them to a hazardous waste collection center"
        "- Mix the chemicals with sand and place them in a sealed container"
    ]),
    (r"(.*)(urban planning in pollution)(.*)", [
        "Role of urban planning in reducing water pollution:\n- Promoting green infrastructure"
        "- Reducing the amount of impervious surfaces, such as roads and parking lots"
    ]),
    (r"(.*)(sustainable fishing)(.*)", [
        "Key principles of sustainable fishing in rivers and oceans:\n- Fish only what you need to eat",
        "- Avoid fishing during spawning season\n- Release any fish that you do not intend to keep\n- Use barbless hooks and release fish carefully"
    ]),
    (r"(.*)(plastic pollution impact | plastic pollution)(.*)", [
        "Impact of plastic pollution on marine life:\n- Plastic pollution can entangle marine animals, causing them to drown or starve"
        "- Marine animals can mistake plastic for food and ingest it\n- It breaks down into tiny pieces called microplastics"
    ]),
    (r"(.*)(wastewater treatment | reuse water)(.*)", [
        "Best practices for wastewater treatment in small communities:\n- Using lagoons"
        "- Sequencing batch reactors\n- Activated sludge processes"
    ]),
    (r"(.*)(climate change water impact | climate change)(.*)", [
        "How climate change affects water bodies and their cleanliness:\n- Climate change can lead to more extreme weather events"
        "- Such as droughts and floods, which can impact water quality and availability\n- Rising sea levels, which can inundate coastal wetlands and estuaries"
    ]),
    (r"(.*)(prevent invasive species)(.*)", [
        "Ways to prevent the spread of invasive aquatic species:\n- Cleaning your boat and trailer thoroughly after each use"
        "- Avoiding transporting live fish or plants between water bodies\n- Reporting any sightings of invasive species to the authorities"
    ]),
    (r"(.*)(groundwater pollution challenges | groundwater pollution)(.*)", [
        "Challenges of managing groundwater pollution:\n- Reducing the use of pesticides and fertilizers"
        "- Lack of monitoring or well\n- Multiple sources of contamination\n- Resource constraints\n- Technological limitations"
    ]),
    (r"(.*)(land erosion water pollution)(.*)", [
        "How land erosion contributes to water pollution:\n- Nutrient loading\n- Habitat disruption"
        "- Chemical contaminants\n- Loss of fertility\n- Increased flooding risk"
    ]),
    (r"(.*)(river pollution sources | how does river get polluted)(.*)", [
        "Main sources of pollution in rivers:\n- Industrial Waste\n- Marine Dumping\n- Sewage and Wastewater"
        "- Oil Leaks and Spills\n- Agriculture\n- Global Warming\n- Radioactive Waste"]),
    (r"(.*)(water quality|home|advanced technologies)(.*)", ["You can check water quality at home by observing clarity, odor, and particles."]),
    (r"(.*)(pollution in nearby river|chatbot)(.*)", ["Contact Central Pollution Control Board for reporting: Parivesh Bhawan, East Arjun Nagar, Delhi-110032, EPABX No.+91-11-43102030, E-mail ccb.cpcb@nic.in"]),
    (r"(.*)(main sources|pollution in rivers)(.*)", ["Major pollution sources include industrial waste, marine dumping, sewage, oil spills, agriculture, global warming, and radioactive waste."]),
    (r"(.*)(tips|reduce water pollution|community level)(.*)", ["Monitor and Regulate Pollution Sources, Educate and Raise Awareness, Support Wastewater Treatment, Reduce Thermal Pollution, Support Legislation and Regulations, Participate in Cleanup Efforts, Properly Dispose of Hazardous Waste, Minimize Chemical Usage, Control Erosion, Properly Manage Stormwater, Maintain Your Vehicle, Reduce Plastic Waste, Upgrade and Maintain Septic Systems, Promote Sustainable Agriculture, Implement Industrial Best Practices."]),
    (r"(.*)(clean up and restore|polluted rivers)(.*)", ["Efforts by organizations like the Central Pollution Control Board (CPCB), State Pollution Control Boards (SPCBs), Pollution Control Committees (PCCs), and Central Water Commission (CWC) are cleaning up polluted rivers."]),
    (r"(.*)(local river cleanup|volunteering)(.*)", ["You can get involved with organizations like Water.org, WaterAid, World Wildlife Fund (WWF), Charity: Water, The Nature Conservancy, UNICEF Water, Sanitation, and Hygiene (WASH) Program, and Water For People for local river cleanup efforts."]),
    (r"(.*)(recent initiatives|projects|water body cleanliness)(.*)", ["Recent initiatives include Namami Gange, Swachh Bharat Mission (SBM), Amrit Sarovar Mission, River Rejuvenation Program, Clean Lake Program, Catch the Rain, and Jal Jeevan Mission."]),
    (r"(.*)(eco-friendly practices|industries|prevent water pollution)(.*)", ["Eco-friendly practices for industries include reducing pesticide and herbicide usage, proper waste disposal, water conservation, eco-friendly cleaning products, avoiding single-use plastics, and supporting sustainable businesses."]),
    (r"(.*)(potential health risks|contaminated water bodies)(.*)", ["Contaminated water can lead to gastrointestinal illnesses, skin infections, and respiratory infections."]),
    (r"(.*)(grants|funding opportunities|water body cleanup projects)(.*)", ["Funding opportunities for water body cleanup projects include the National River Conservation Plan, Clean Ganga Fund, corporate social responsibility, Arghyam, Vasundhara Foundation, Waste Warriors, Environmentalist Foundation of India, Goonj, and the River Connect Campaign."]),
    (r"(.*)(tell if local water body|polluted)(.*)", ["Signs of pollution in local water bodies include unusual odor, scum, unusual behavior of aquatic animals, excessive algae growth, presence of plastic and litter, and discolored water."]),
    (r"(.*)(impact of pollution|aquatic ecosystems|wildlife)(.*)", ["Pollution impacts aquatic ecosystems and wildlife through loss of biodiversity, habitat destruction, poisoning of water bodies, disruption of the food chain, and reduced economic value."]),
    (r"(.*)(recommend eco-friendly products|individuals|water bodies)(.*)", ["Eco-friendly practices near water bodies include not submerging chemical-containing items, avoiding trash disposal in water bodies, and protecting aquatic habitats."]),
    (r"(.*)(website|receive alerts|cleanliness drives)(.*)", ["Websites like mygov.in and swechha.in provide alerts for cleanliness drives."]),
    (r"(.*)(consequences|industrial waste discharges|rivers)(.*)", ["Consequences of industrial waste discharges in rivers include harm to aquatic life, human health, and safety for recreation."]),
    (r"(.*)(common pollutants|urban areas)(.*)", ["Common water pollutants in urban areas include oil, grease, heavy metals, pesticides, fertilizers, bacteria, viruses, sediment, and trash."]),
    (r"(.*)(importance|wetlands|water body protection)(.*)", ["Wetlands serve as natural filters, removing pollutants from water and providing habitats for fish, birds, and other wildlife."]),
    (r"(.*)(measures|communities|prevent lake eutrophication)(.*)", ["Communities can prevent lake eutrophication by reducing nutrient input, diverting stormwater, and planting trees and vegetation to filter runoff."]),
    (r"(.*)(safely dispose|old household cleaning chemicals)(.*)", ["Safely dispose of old household chemicals by taking them to a hazardous waste collection center or mixing them with sand in a sealed container."]),
    (r"(.*)(role|urban planning|reduce water pollution)(.*)", ["Urban planning can reduce water pollution by promoting green infrastructure and reducing impervious surfaces like roads and parking lots."]),
    (r"(.*)(key principles|sustainable fishing|rivers|oceans)(.*)", ["Key principles of sustainable fishing include fishing what you need to eat, avoiding fishing during spawning season, releasing unwanted fish, and using barbless hooks."]),
    (r"(.*)(impact|plastic pollution|marine life)(.*)", ["Plastic pollution impacts marine life by causing entanglement, ingestion, and breakdown into microplastics."]),
    (r"(.*)(best practices|wastewater treatment|small communities)(.*)", ["Best practices for small community wastewater treatment include using lagoons, sequencing batch reactors, and activated sludge processes."]),
    (r"(.*)(climate change affect|water bodies|cleanliness)(.*)", ["Climate change can affect water bodies by causing extreme weather events, droughts, floods, and rising sea levels."]),
    (r"(.*)(prevent spread|invasive aquatic species)(.*)", ["Prevent the spread of invasive species by cleaning your boat, avoiding transporting live fish or plants, and reporting sightings to authorities."]),
    (r"(.*)(challenges|managing groundwater pollution)(.*)", ["Challenges in managing groundwater pollution include reducing pesticide and fertilizer use, lack of monitoring, multiple contamination sources, resource constraints, and technological limitations."]),
    (r"(.*)(land erosion contribute|water pollution)(.*)", ["Land erosion contributes to water pollution through nutrient loading, habitat disruption, chemical contaminants, loss of fertility, and increased flooding risk."]),
    (r"(.*)(main sources|pollution|rivers)(.*)", ["Common sources of pollution in rivers include cleaning products, personal hygiene products, medications, pesticides, insecticides, paints, solvents, motor oils, plastic bags, microplastics, and e-waste."]),
    (r"(.*)(grants|funding opportunities|water body cleanup projects)(.*)", ["Grants and funding opportunities for water body cleanup projects include the National River Conservation Plan, Clean Ganga Fund, corporate social responsibility, Arghyam, Vasundhara Foundation, Waste Warriors, Environmentalist Foundation of India, Goonj, and the River Connect Campaign."]),
    (r"(.*)(tell if local water body|polluted)(.*)", ["Signs of a polluted local water body include unusual odor, scum, unusual behavior of aquatic animals, excessive growth of algae, presence of plastic, litter, and discolored water."]),
    (r"(.*)(impact of pollution|aquatic ecosystems|wildlife)(.*)", ["Pollution's impact on aquatic ecosystems and wildlife includes loss of biodiversity, habitat destruction, poisoning of water bodies, disruption of the food chain, and reduced economic value."]),
    (r"(.*)(recommend eco-friendly products|individuals|water bodies)(.*)", ["Eco-friendly practices near water bodies include avoiding chemical submersion, proper trash disposal, and protection of aquatic habitats."]),
    (r"(.*)(website|receive alerts|cleanliness drives)(.*)", ["Websites like mygov.in and swechha.in provide alerts for cleanliness drives."]),
    (r"(.*)(consequences|industrial waste discharges|rivers)(.*)", ["Consequences of industrial waste discharges into rivers include harm to aquatic life, human health, and safety for recreation."]),
    (r"(.*)(common pollutants|urban areas)(.*)", ["Common pollutants in urban areas include oil, grease, heavy metals, pesticides, fertilizers, bacteria, viruses, sediment, and trash."]),
    (r"(.*)(importance|wetlands|water body protection)(.*)", ["Wetlands play a vital role in water body protection, acting as natural filters, removing pollutants, and providing habitats for fish, birds, and other wildlife."]),
    (r"(.*)(measures|communities|prevent lake eutrophication)(.*)", ["Communities can prevent lake eutrophication by reducing nutrient input, diverting stormwater, and planting trees and vegetation to filter runoff."]),
    (r"(.*)(safely dispose|old household cleaning chemicals)(.*)", ["Safely dispose of old household cleaning chemicals by taking them to a hazardous waste collection center or mixing them with sand in a sealed container."]),
    (r"(.*)(role|urban planning|reduce water pollution)(.*)", ["Urban planning can reduce water pollution by promoting green infrastructure and reducing impervious surfaces like roads and parking lots."]),
    (r"(.*)(key principles|sustainable fishing|rivers|oceans)(.*)", ["Key principles of sustainable fishing include fishing only what you need, avoiding fishing during spawning season, releasing fish you don't intend to keep, and using barbless hooks."]),
    (r"(.*)(impact|plastic pollution|marine life)(.*)", ["Plastic pollution has a significant impact on marine life, leading to entanglement, ingestion, and the formation of microplastics."]),
    (r"(.*)(best practices|wastewater treatment|small communities)(.*)", ["Best practices for wastewater treatment in small communities include using lagoons, sequencing batch reactors, and activated sludge processes."]),
    (r"(.*)(climate change affect|water bodies|cleanliness)(.*)", ["Climate change can affect water bodies by causing more extreme weather events, droughts, floods, and rising sea levels."]),
    (r"(.*)(prevent spread|invasive aquatic species)(.*)", ["To prevent the spread of invasive aquatic species, clean your boat and trailer, avoid transporting live fish or plants between water bodies, and report sightings to authorities."]),
    (r"(.*)(challenges|managing groundwater pollution)(.*)", ["Challenges in managing groundwater pollution include reducing pesticide and fertilizer use, lack of monitoring, multiple sources of contamination, resource constraints, and technological limitations."]),
    (r"(.*)(land erosion contribute|water pollution)(.*)", ["Land erosion contributes to water pollution through nutrient loading, habitat disruption, chemical contaminants, loss of fertility, and increased flooding risk."]),
    (r"(.*)(citizen reporting|pollution control)(.*)", ["Citizen reporting is essential for identifying pollution incidents and enabling timely responses and enforcement."]),
    (r"(.*)(innovative technologies|water purification)(.*)", ["Innovative water purification technologies include UV disinfection and membrane filtration."]),
    (r"(.*)(recommend eco-friendly products|river cleanup)(.*)", ["Eco-friendly cleanup products include biodegradable trash bags and non-toxic cleaning solutions."]),
    (r"(.*)(role|river restoration|climate change mitigation)(.*)", ["River restoration can mitigate climate change by enhancing carbon sequestration and reducing pollution."]),
    (r"(.*)(river conservation programs|students)(.*)", ["River conservation programs for students educate them about clean water and ecosystems."]),
    (r"(.*)(urban forests|water conservation)(.*)", ["Urban forests contribute to water conservation by capturing rainwater and reducing runoff."]),
    (r"(.*)(practices|prevent chemical runoff|rivers)(.*)", ["Practices to prevent chemical runoff include proper storage, disposal, and using eco-friendly alternatives."]),
    (r"(.*)(potable water sources|emergency)(.*)", ["Potable water sources can be accessed in emergencies through local authorities and relief organizations."]),
    (r"(.*)(impact|agricultural runoff|water bodies)(.*)", ["Agricultural runoff impacts water bodies through algae blooms, eutrophication, and harm to aquatic life."]),
    (r"(.*)(importance|riparian zones|water quality)(.*)", ["Riparian zones are vital for maintaining water quality by filtering pollutants and preventing erosion."]),
    (r"(.*)(reduce water usage|household)(.*)", ["You can reduce household water usage by fixing leaks, taking shorter showers, turning off faucets when brushing, watering lawns less, and using water-efficient appliances."]),
    (r"(.*)(efforts|corporate responsibility|water conservation)(.*)", ["Corporate social responsibility efforts can contribute to water conservation through sustainable practices."]),
    (r"(.*)(explain|importance of riparian areas|river ecosystems)(.*)", ["Riparian areas are crucial for river ecosystems as they provide habitats, filter pollutants, and reduce erosion."]),
    (r"(.*)(strategies|urban water management|reduce waste)(.*)", ["Urban water management strategies aim to reduce waste through recycling, conservation, and efficient infrastructure."]),
    (r"(.*)(measures|improve river water quality)(.*)", ["Measures to improve river water quality include reducing pollution sources, promoting conservation, and enacting regulations."]),
    (r"(.*)(major threats|aquatic biodiversity|pollution)(.*)", ["Major threats to aquatic biodiversity due to pollution include habitat destruction, population decline, and species extinction."]),
    (r"(.*)(ecological benefits|wetland preservation|water bodies)(.*)", ["Preserving wetlands provides ecological benefits like flood control, wildlife habitats, and water purification for nearby water bodies."]),
    (r"(.*)(clean rivers|economic benefits)(.*)", ["Clean rivers lead to economic benefits through increased tourism, recreational activities, and improved property values."]),
    (r"(.*)(residential water usage|conservation tips)(.*)", ["Tips for conserving water in residences include fixing leaks, using low-flow fixtures, and adopting water-saving habits."]),
    (r"(.*)(impact of deforestation|rivers)(.*)", ["Deforestation negatively impacts rivers by increasing sediment runoff, reducing water quality, and disrupting ecosystems."]),
    (r"(.*)(wastewater recycling|sustainable practices)(.*)", ["Wastewater recycling contributes to sustainable practices by reusing treated water for non-potable purposes."]),
    (r"(.*)(signs|water contamination|health risks)(.*)", ["Signs of water contamination may lead to health risks such as gastrointestinal illnesses, skin infections, and respiratory problems."]),
    (r"(.*)(recreational activities|rivers|environmental responsibility)(.*)", ["Engaging in recreational activities on rivers should be done with environmental responsibility to minimize pollution and disturbance to aquatic life."]),
    (r"(.*)(drinking water|home purification)(.*)", ["You can ensure safe drinking water at home by using water purifiers and filters."]),
    (r"(.*)(reducing water usage|smart irrigation)(.*)", ["Smart irrigation systems help in reducing water usage for maintaining lawns and gardens."]),
    (r"(.*)(address|pollution|industrial sites)(.*)", ["Addressing pollution from industrial sites involves stricter regulations, pollution control technologies, and corporate responsibility."]),
    (r"(.*)(effect of climate change|rivers|water levels)(.*)", ["Climate change can affect rivers by altering water levels and impacting ecosystems."]),
    (r"(.*)(wildlife protection|river ecosystems)(.*)", ["Protecting river ecosystems is essential for the conservation of wildlife species, such as fish, birds, and aquatic organisms."]),
    (r"(.*)(water conservation apps|smart devices)(.*)", ["Water conservation apps and smart devices can help monitor and manage water usage efficiently."]),
    (r"(.*)(monitor water quality|DIY tests)(.*)", ["You can monitor water quality using DIY tests that check for parameters like pH, turbidity, and contaminants."]),
    (r"(.*)(benefits|rainwater harvesting)(.*)", ["Rainwater harvesting provides benefits like water conservation, reduced utility bills, and self-sufficiency."]),
    (r"(.*)(human activities|river pollution)(.*)", ["Human activities contribute to river pollution through industrial discharges, sewage, and agricultural runoff."]),
    (r"(.*)(reduce water wastage|efficient fixtures)(.*)", ["Reducing water wastage is possible by using efficient fixtures like low-flow toilets and showerheads."]),
    (r"(.*)(measures|protect aquatic habitats)(.*)", ["Measures to protect aquatic habitats include creating marine reserves, enforcing fishing regulations, and reducing pollution."]),
    (r"(.*)(drinking water standards|EPA)(.*)", ["Drinking water standards in the United States are regulated by the Environmental Protection Agency (EPA)."]),
    (r"(.*)(pollutants|toxic chemicals|rivers)(.*)", ["Toxic chemicals like heavy metals and pesticides are common pollutants in rivers."]),
    (r"(.*)(safe disposal|household hazardous waste)(.*)", ["Safe disposal of household hazardous waste involves taking it to designated collection centers."]),
    (r"(.*)(report water pollution|local authorities)(.*)", ["Report water pollution incidents to local environmental or water quality authorities for investigation and action."]),
    (r"(.*)(river water contamination|human health risks)(.*)", ["Contaminated river water poses health risks, including gastrointestinal illnesses and waterborne diseases."]),
    (r"(.*)(chemical runoff|stormwater management)(.*)", ["Effective stormwater management helps prevent chemical runoff and protects water bodies."]),
    (r"(.*)(groundwater pollution prevention|best practices)(.*)", ["Preventing groundwater pollution involves best practices like reducing chemical usage and implementing monitoring systems."]),
    (r"(.*)(pollution effects|aquatic ecosystems)(.*)", ["Pollution has adverse effects on aquatic ecosystems, leading to habitat destruction and species decline."]),
    (r"(.*)(water conservation regulations|government policies| govt policies)(.*)", ["Government policies and regulations play a significant role in water conservation efforts."]),
    (r"(.*)(nutrient pollution|water quality issues)(.*)", ["Nutrient pollution causes water quality issues like eutrophication, algae blooms, and harm to aquatic life."]),
    (r"(.*)(environmental organizations|river conservation)(.*)", ["Environmental organizations are actively involved in river conservation efforts to protect aquatic environments."]),
    (r"(.*)(stormwater runoff|urban areas)(.*)", ["Stormwater runoff in urban areas carries pollutants like oil, chemicals, and debris into water bodies."]),
    (r"(.*)(water scarcity solutions|desalination)(.*)", ["Desalination is one of the solutions to address water scarcity by converting seawater into freshwater."]),
    (r"(.*)(riverbank erosion|mitigation methods)(.*)", ["Mitigation methods for riverbank erosion include revetments, riprap, and vegetation planting."]),
    (r"(.*)(water conservation techniques|xeriscaping)(.*)", ["Xeriscaping is an effective water conservation technique that uses drought-resistant plants and efficient irrigation."]),
    (r"(.*)(toxic algae blooms|health hazards)(.*)", ["Toxic algae blooms in water bodies can lead to health hazards like skin rashes and respiratory issues."]),
    (r"(.*)(wastewater treatment processes|sewage)(.*)", ["Sewage undergoes wastewater treatment processes like primary, secondary, and tertiary treatment to remove contaminants."]),
    (r"(.*)(climate change adaptation|rivers|flooding)(.*)", ["Adaptation to climate change impacts includes addressing flooding risks in river areas."]),
    (r"(.*)(water conservation tips|bathroom)(.*)", ["Water conservation tips for the bathroom include using low-flow fixtures and fixing leaks."]),
    (r"(.*)(river water monitoring|water quality)(.*)", ["Regular monitoring of river water is essential to assess water quality and detect pollution incidents."]),
    (r"(.*)(waterborne diseases|contaminated water)(.*)", ["Contaminated water can lead to waterborne diseases such as cholera, typhoid, and gastroenteritis."]),
    (r"(.*)(river restoration projects|ecosystem health)(.*)", ["River restoration projects aim to improve ecosystem health by enhancing water quality and habitats."]),
    (r"(.*)(impact of litter|water pollution)(.*)", ["Litter contributes to water pollution by releasing toxins, affecting aquatic life, and degrading water quality."]),
    (r"(.*)(residential rain barrels|rainwater harvesting)(.*)", ["Residential rain barrels are used for rainwater harvesting to conserve water for non-potable purposes."]),
    (r"(.*)(citizen initiatives|river cleanup)(.*)", ["Citizen initiatives play a vital role in river cleanup by organizing clean-up events and raising awareness."]),
    (r"(.*)(water recycling systems|industrial facilities)(.*)", ["Industrial facilities use water recycling systems to reduce water consumption and discharge."]),
    (r"(.*)(water conservation practices|drought conditions)(.*)", ["Water conservation practices are crucial during drought conditions to manage water resources efficiently."]),
    (r"(.*)(aquatic biodiversity conservation|habitat preservation)(.*)", ["Conserving aquatic biodiversity involves preserving natural habitats, reducing pollution, and sustainable management."]),
    (r"(.*)(graywater recycling|household use)(.*)", ["Graywater recycling allows households to reuse wastewater for purposes like irrigation."]),
    (r"(.*)(smart meters|water consumption monitoring)(.*)", ["Smart meters help in monitoring water consumption and identifying leaks in real-time."]),
    (r"(.*)(drinking water contamination|water treatment)(.*)", ["Water treatment processes help in removing contaminants and ensuring safe drinking water."]),
    (r"(.*)(reduce agricultural runoff|best practices)(.*)", ["Best practices to reduce agricultural runoff include using buffer zones, cover crops, and reducing chemical use."]),
    (r"(.*)(sedimentation|river water quality)(.*)", ["Sedimentation affects river water quality by increasing turbidity and carrying pollutants."]),
    (r"(.*)(water conservation grants|government support| govt support)(.*)", ["Government grants and support are available for water conservation projects and initiatives."]),
    (r"(.*)(fish population decline|pollution impacts)(.*)", ["Fish population decline is a consequence of pollution impacts like habitat loss and water toxicity."]),
    (r"(.*)(riverbank vegetation|erosion control)(.*)", ["Riverbank vegetation is crucial for erosion control and stabilizing riverbanks."]),
    (r"(.*)(marine conservation|pollution prevention)(.*)", ["Marine conservation efforts focus on preventing pollution, protecting ecosystems, and marine species."]),
    (r"(.*)(residential water audits|efficiency improvement)(.*)", ["Residential water audits identify areas for efficiency improvement in water usage."]),
    (r"(.*)(groundwater protection|well maintenance)(.*)", ["Protecting groundwater requires well maintenance and proper disposal of hazardous materials."]),
    (r"(.*)(impact of invasive species|rivers|ecosystems)(.*)", ["Invasive species negatively impact rivers and ecosystems by outcompeting native species and altering habitats."]),
    (r"(.*)(drinking water sources|contamination risks)(.*)", ["Contamination risks to drinking water sources can arise from industrial discharges, agricultural runoff, and sewage pollution."]),
    (r"(.*)(riverbank stabilization|natural methods)(.*)", ["Natural methods for riverbank stabilization include planting native vegetation and using bioengineering techniques."]),
    (r"(.*)(stream buffers|protect water quality)(.*)", ["Stream buffers protect water quality by filtering pollutants and stabilizing streambanks."]),
    (r"(.*)(water-efficient appliances|home upgrades)(.*)", ["Upgrading to water-efficient appliances is an effective home upgrade to conserve water."]),
    (r"(.*)(river ecosystems|ecological services)(.*)", ["River ecosystems provide ecological services such as water purification, flood control, and wildlife habitats."]),
    (r"(.*)(aquatic habitat destruction|pollution)(.*)", ["Pollution contributes to aquatic habitat destruction by contaminating water and reducing biodiversity."]),
    (r"(.*)(sustainable agriculture practices|water conservation)(.*)", ["Sustainable agriculture practices promote water conservation by reducing chemical use and improving soil health."]),
    (r"(.*)(stream restoration|ecosystem health)(.*)", ["Stream restoration projects enhance ecosystem health by improving water quality and fish habitats."]),
    (r"(.*)(microplastic pollution|marine environment)(.*)", ["Microplastic pollution impacts the marine environment by entering the food chain and affecting aquatic life."]),
    (r"(.*)(home water filtration systems|safe drinking water)(.*)", ["Home water filtration systems ensure safe drinking water by removing contaminants and impurities."]),
    (r"(.*)(water conservation tips|outdoor activities)(.*)", ["Water conservation tips for outdoor activities include reducing water usage for gardening and car washing."]),
    (r"(.*)(river water pollution|community involvement)(.*)", ["Community involvement is essential to address river water pollution by participating in cleanup efforts and reporting incidents."]),
    (r"(.*)(emergency preparedness|water storage)(.*)", ["Emergency preparedness involves water storage to ensure a safe supply in case of disasters or disruptions."]),
    (r"(.*)(ecological consequences|acid rain|aquatic ecosystems)(.*)", ["Acid rain has ecological consequences on aquatic ecosystems by reducing water pH and harming aquatic life."]),
    (r"(.*)(safe swimming practices|rivers)(.*)", ["Safe swimming practices in rivers include checking water quality, avoiding strong currents, and wearing appropriate gear."]),
    (r"(.*)(water conservation habits|daily life)(.*)", ["Incorporating water conservation habits into daily life includes turning off taps when not in use and repairing leaks."]),
    (r"(.*)(low-impact landscaping|water-friendly plants)(.*)", ["Low-impact landscaping involves using water-friendly plants and xeriscaping to conserve water in yards."]),
    (r"(.*)(water pollution prevention|individual responsibility)(.*)", ["Water pollution prevention is a shared responsibility involving individuals in protecting water bodies."]),
    (r"(.*)(urban river restoration|public spaces)(.*)", ["Urban river restoration transforms public spaces into vibrant and sustainable waterfronts."]),
    (r"(.*)(drinking water access|global water initiatives)(.*)", ["Global water initiatives like Water.org and UNICEF work to improve drinking water access in underserved communities."]),
    (r"(.*)(urban planning|riverfront development)(.*)", ["Urban planning plays a critical role in riverfront development, ensuring a balance between development and conservation."]),
    (r"(.*)(aquatic biodiversity|role of wetlands)(.*)", ["Wetlands play a significant role in preserving aquatic biodiversity by providing habitat and food sources for various species."]),
    (r"(.*)(public awareness campaigns|water conservation)(.*)", ["Public awareness campaigns are vital for promoting water conservation and fostering a sense of responsibility."]),
    (r"(.*)(water quality testing|community initiatives)(.*)", ["Community initiatives can conduct water quality testing to identify pollution sources and protect local water bodies."]),
    (r"(.*)(source protection|watershed management)(.*)", ["Watershed management includes source protection to ensure clean and safe water resources."]),
    (r"(.*)(protecting coastal areas|pollution prevention)(.*)", ["Protecting coastal areas is crucial for pollution prevention to safeguard marine environments."]),
    (r"(.*)(industrial discharge|pollution control measures)(.*)", ["Pollution control measures for industrial discharge involve treatment technologies and regulatory compliance."]),
    (r"(.*)(community engagement|river cleanup efforts)(.*)", ["Community engagement enhances the success of river cleanup efforts by involving local residents and organizations."]),
    (r"(.*)(pharmaceutical waste disposal|environmentally friendly)(.*)", ["Proper pharmaceutical waste disposal includes environmentally friendly methods to prevent contamination of water bodies."]),
    (r"(.*)(conservation practices|residential rain gardens)(.*)", ["Conservation practices like residential rain gardens help manage stormwater and enhance local water quality."]),
    (r"(.*)(water scarcity|sustainable water use)(.*)", ["Addressing water scarcity requires sustainable water use practices and efficient water management."]),
    (r"(.*)(climate change effects|water resources)(.*)", ["Climate change effects on water resources include alterations in precipitation patterns and water availability."]),
    (r"(.*)(sustainable fishing|local communities)(.*)", ["Practicing sustainable fishing supports local communities by preserving fish populations and ecosystems."]),
    (r"(.*)(plastic waste reduction|marine conservation)(.*)", ["Reducing plastic waste is essential for marine conservation and protecting aquatic life."]),
    (r"(.*)(wastewater treatment|small municipalities)(.*)", ["Wastewater treatment solutions for small municipalities include cost-effective and efficient systems."]),
    (r"(.*)(watershed protection|natural habitats)(.*)", ["Watershed protection safeguards natural habitats and enhances water quality in the surrounding region."]),
    (r"(.*)(water pollution education|schools)(.*)", ["Water pollution education in schools instills awareness and responsibility for conserving water bodies."]),
    (r"(.*)(river restoration funding|nonprofit organizations)(.*)", ["Nonprofit organizations often provide river restoration funding to support conservation initiatives."]),
    (r"(.*)(urban development|riverfront rehabilitation)(.*)", ["Urban development projects may include riverfront rehabilitation to revitalize waterfront areas."]),
    (r"(.*)(water conservation policy|government initiatives| govt initiatives)(.*)", ["Government initiatives establish water conservation policies and regulations to protect water resources."]),
    (r"(.*)(aquatic life conservation|wetland restoration)(.*)", ["Wetland restoration contributes to aquatic life conservation by recreating critical habitats."]),
    (r"(.*)(effective water management|watershed councils)(.*)", ["Effective water management involves collaboration with watershed councils and local stakeholders."]),
    (r"(.*)(clean energy technologies|water desalination)(.*)", ["Clean energy technologies support water desalination as a sustainable solution for water scarcity."]),    
]
def respond_to_input(user_input):
    for pattern, responses in pairs:
        if re.match(pattern, user_input, re.IGNORECASE):
            return responses
    return ["I'm not sure how to respond to that"]

st.title("Lanturn AI")

recognizer = sr.Recognizer()
tmp_audio_file = None
enter_pressed = False  # Initialize the Enter key flag

def set_dynamic_energy_threshold(source):
    with source as audio_source:
        recognizer.adjust_for_ambient_noise(audio_source)
        energy_threshold = recognizer.energy_threshold
    return energy_threshold

def capture_audio(energy_threshold):
    with sr.Microphone(device_index=None) as source:
        recognizer.energy_threshold = energy_threshold
        audio = recognizer.listen(source, timeout=5)
    return audio

# Check if a microphone is available
def is_microphone_available():
    try:
        available_microphones = sr.Microphone.list_microphone_names()
        return len(available_microphones) > 0
    except OSError:
        return False

user_input = st.text_input("Enter text or click the 🎙️ Record Speech button to speak:", key="user_input")

if st.button("🎙️ Record Speech"):
    if is_microphone_available():
        try:
            st.write("Listening...")
            energy_threshold = set_dynamic_energy_threshold(sr.Microphone(device_index=None))
            audio = capture_audio(energy_threshold)
            user_speech = recognizer.recognize_google(audio)
            
            # Set recognized speech as the value of the text input
            user_input = user_speech
            st.text_area("You (speech):", value=user_speech, key="user_speech", height=100)
        except sr.UnknownValueError:
            st.write("I could not understand the audio.")
        except sr.RequestError as e:
            st.write(f"Error: {e}")
    else:
        st.write("No microphone available. Please check your microphone configuration.")

if st.button("Submit") or enter_pressed:
    enter_pressed = False
    if user_input.lower() == "exit":
        st.write("Chatbot: Goodbye!")
    else:
        responses = respond_to_input(user_input)
        chatbot_response = responses[0]
        st.write("Chatbot:", chatbot_response)

        tts = gTTS(chatbot_response)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_audio_file:
            tts.save(tmp_audio_file.name)

        audio_clip = mp.AudioFileClip(tmp_audio_file.name)
        video_clip = mp.VideoFileClip("talkingreal.mp4")  # Replace with your video file

        if audio_clip.duration > video_clip.duration:
            num_loops = int(audio_clip.duration / video_clip.duration) + 1
            video_clip_loop = mp.concatenate_videoclips([video_clip] * num_loops)
            video_clip_loop = video_clip_loop.subclip(0, audio_clip.duration)
            combined_clip = video_clip_loop.set_audio(audio_clip)
        else:
            combined_clip = video_clip.set_audio(audio_clip)
            combined_clip = combined_clip.set_duration(audio_clip.duration)  # Set video duration to match audio

        # Save the combined video to a temporary file
        combined_video_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
        combined_clip.write_videofile(combined_video_path, codec="libx264", audio_codec="aac")

        # Display the video using HTML and control its size with custom CSS
        st.markdown(f'<video src="data:video/mp4;base64,{base64.b64encode(open(combined_video_path, "rb").read()).decode()}" autoplay controls style="width:100%"></video>', unsafe_allow_html=True)
