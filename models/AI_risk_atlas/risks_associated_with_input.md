# Data bias risk for AI
Description
Historical, representational, and societal biases present in the data used to train and fine tune the model can adversely affect model behavior.

Why is data bias a concern for foundation models?
Training an AI system on data with bias, such as historical or representational bias, could lead to biased or skewed outputs that may unfairly represent or otherwise discriminate against certain groups or individuals. In addition to negative societal impacts, business entities could face legal consequences or reputational harms from biased model outcomes.

Example
Healthcare Bias

According to the research article on reinforcing disparities in medicine using data and AI applications to transform how people receive healthcare is only as strong as the data behind the effort. For example, using training data with poor minority representation or that reflects what is already unequal care can lead to increased health inequalities.

Sources:
Forbes, December 2022

# Data poisoning risk for AI
Description
A type of adversarial attack where an adversary or malicious insider injects intentionally corrupted, false, misleading, or incorrect samples into the training or fine-tuning dataset.

Why is data poisoning a concern for foundation models?
Poisoning data can make the model sensitive to a malicious data pattern and produce the adversary’s desired output. It can create a security risk where adversaries can force model behavior for their own benefit. In addition to producing unintended and potentially malicious results, a model misalignment from data poisoning can result in business entities facing legal consequences or reputational harms.

# Data curation risk for AI
Description
When training or tuning data is improperly collected or prepared, the result can be a misalignment of a model's desired values or intent and the actual outcome.

Why is data curation a concern for foundation models?
Improper data curation can adversely affect how a model is trained, resulting in a model that does not behave in accordance with the intended values. Correcting problems after the model is trained and deployed might be insufficient for guaranteeing proper behavior. Improper model behavior can result in business entities facing legal consequences or reputational harms.

# Downstream retraining risk for AI
Description
Using undesirable (for example, inaccurate, inappropriate, user’s content) output from downstream applications for retraining purposes.

Why is downstream retraining a concern for foundation models?
Repurposing downstream output for retraining a model without implementing proper human vetting increases the chances of undesirable outputs being incorporated into the training or tuning data of the model. This, in turn, can generate even more undesirable output. Improper model behavior can result in business entities facing legal consequences or reputational harms. Failing to comply with data transfer laws might result in fines and other legal consequences.

Example
Model collapse due to training using AI-generated content

As stated in the source article, a group of researchers from the UK and Canada investigated the problem of using AI-generated content for training instead of human-generated content. They found that the large language models behind the technology might potentially be trained on other AI-generated content. As generated data continues to spread in droves across the internet it can result ina phenomenon they coined as "model collapse."

Sources:
Business Insider, August 2023

# Data transfer risk for AI
Description
Laws and other restrictions can limit or prohibit transferring data.

Why is data transfer a concern for foundation models?
Data transfer restrictions can impact the availability of the data that is required for training an AI model and can lead to poorly represented data. In addition to impact on data availability, failure to comply with data transfer laws and regulations might result in fines and other legal consequences.

Example
Data Restriction Laws

As stated in the research article, data localization measures, which restrict the ability to move data globally reduce the capacity to develop tailored AI capacities. It affects AI directly by providing less training data and indirectly by undercutting the building blocks on which AI is built.

Examples include China's data localization laws, and GDPR restrictions on the processing and use of personal data.

Sources:
Brookings, December 2018

# Data usage risk for AI
Description
Laws and other restrictions can limit or prohibit the use of some data for specific AI use cases.

Why is data usage a concern for foundation models?
Failing to comply with data usage laws might result in fines and other legal consequences.

# Data acquisition risk for AI
Description
Laws and other regulations might limit the collection of certain types of data for specific AI use cases.

Why is data acquisition a concern for foundation models?
Failing to comply with data acquisition laws and regulations might result in fines and other legal consequences.

# Data usage rights risk for AI
Description
Terms of service, copyright laws, or other rules restrict the ability to use certain data for building models.

Why is data usage rights a concern for foundation models?
Laws and regulations concerning the use of data to train AI are unsettled and can vary from country to country, which creates challenges in the development of models. If data usage violates rules or restrictions, business entities might face fines, reputational harms, and other legal consequences.

Example
Text Copyright Infringement Claims

According to the source article, The New York Times sued OpenAI and Microsoft, accusing them accusing them of using millions of the newspaper's articles without permission to help train chatbots to provide information to readers.

Sources:
Reuters, December 2023

# Confidential information in data risk for AI
Description
Models might be trained or fine-tuned using confidential data or the company’s intellectual property, which could result in unwanted disclosure of that information.

Why is confidential information in data a concern for foundation models?
If not developed in accordance with data protection rules and regulations, the model might expose confidential information or IP in the generated output or through an adversarial attack.

# Data transparency risk for AI
Description
Without accurate documentation on how a model's data was collected, curated, and used to train a model, it might be harder to satisfactorily explain the behavior of the model with respect to the data.

Why is data transparency a concern for foundation models?
Data transparency is important for legal compliance and AI ethics. Missing information limits the ability to evaluate risks associated with the data. The lack of standardized requirements might limit disclosure as organizations protect trade secrets and try to limit others from copying their models.

Example
Data and Model Metadata Disclosure

OpenAI's technical report is an example of the dichotomy around disclosing data and model metadata. While many model developers see value in enabling transparency for consumers, disclosure poses real safety issues and might increase the ability to misuse the models. In the GPT-4 technical report, the authors state: “Given both the competitive landscape and the safety implications of large-scale models like GPT-4, this report contains no further details about the architecture (including model size), hardware, training compute, data set construction, training method, or similar.”

Sources:
OpenAI, March 2023

# Data provenance risk for AI
Description
Without standardized and established methods for verifying where data came from, there are no guarantees that available data is what it claims to be.

Why is data provenance a concern for foundation models?
Not all data sources are trustworthy. Data might have been unethically collected, manipulated, or falsified. Using such data can result in undesirable behaviors in the model. Business entities could face fines, reputational harms, and other legal consequences.

# Personal information in data risk for AI
Description
Inclusion or presence of personal identifiable information (PII) and sensitive personal information (SPI) in the data used for training or fine tuning the model might result in unwanted disclosure of that information.

Why is personal information in data a concern for foundation models?
If not properly developed to protect sensitive data, the model might expose personal information in the generated output. Additionally, personal or sensitive data must be reviewed and handled with respect to privacy laws and regulations, as business entities could face fines, reputational harms, and other legal consequences if found in violation.

Example
Training on Private Information

According to the article, Google and its parent company Alphabet were accused in a class-action lawsuit of misusing vast amount of personal information and copyrighted material. The information was taken from hundreds of millions of internet users to train its commercial AI products, which include Bard, its conversational generative artificial intelligence chatbot. This case follows similar lawsuits that are filed against Meta Platforms, Microsoft, and OpenAI over their alleged misuse of personal data.

# Reidentification risk for AI
Description
Even with the removal or personal identifiable information (PII) and sensitive personal information (SPI) from data, it might still be possible to identify persons due to other features available in the data.

Why is reidentification a concern for foundation models?
Data that can reveal personal or sensitive data must be reviewed with respect to privacy laws and regulations, as business entities could face fines, reputational harms, and other legal consequences if found in violation.

# Data privacy rights risk for AI
Description
Challenges around the ability to provide data subject rights such as opt-out, right to access, right to be forgotten.

Why is data privacy rights a concern for foundation models?
The identification or improper usage of data might lead to violation of privacy laws. Improper usage or a request for data removal might force organizations to retrain the model, which is expensive. In addition, business entities might face fines, reputational harms, disruption to operations, and other legal consequences if they fail to comply with data privacy rules and regulations.

Example
Right to Be Forgotten (RTBF)

Laws in multiple locales, including Europe (GDPR), grant data subjects the right to request personal data to be deleted by organizations (‘Right To Be Forgotten’, or RTBF). However, emerging, and increasingly popular large language model (LLM) -enabled software systems present new challenges for this right. According to research by CSIRO’s Data61, data subjects can identify usage of their personal information in an LLM “by either inspecting the original training data set or perhaps prompting the model.” However, training data might not be public, or companies do not disclose it, citing safety and other concerns. Guardrails might also prevent users from accessing the information by prompting. Due to these barriers, data subjects might not be able to initiate RTBF procedures and companies that deploy LLMs might not be able to meet RTBF laws.

Sources:
Zhang et al., September 2023

Example
Lawsuit About LLM Unlearning

According to the report, a lawsuit was filed against Google that alleges the use of copyright material and personal information as training data for its AI systems, which includes its Bard chatbot. Opt-out and deletion rights are guaranteed rights for California residents under the CCPA and children in the United States under the age of 13 with COPPA. The plaintiffs allege that because there is no way for Bard to “unlearn” or fully remove all the scraped PI it has been fed. The plaintiffs note that Bard’s privacy notice states that Bard conversations cannot be deleted by the user after they have been reviewed and annotated by the company and might be kept up to 3 years. P allege that these practices further contribute to noncompliance with these laws.

Sources:
Reuters, July 2023
J.L. v. Alphabet Inc., July 2023

# Informed consent risk for AI
Description
Data collected for training AI models without the owner's informed consent even when it is legally permitted to do so.

Why is informed consent a concern for foundation models?
Under certain circumstances, it might be unethical to collect and use data without the person's consent. There are also possible reputational risks to such use.

Description
Disclosing Personal Information or Sensitive Personal Information as a part of a prompt that is sent to the model.

# Personal information in prompt risk for AI
Why is personal information in prompt a concern for foundation models?
Prompt data might be stored or later used for other purposes like model evaluation and retraining. These types of data must be reviewed with privacy laws and regulations. Without proper data storage and usage business entities might face fines, reputational harms, disruption to operations, and other legal consequences.

Example
Disclose personal health information in ChatGPT prompts

According to the source article, some people on social media shared about using ChatGPT as their makeshift therapists. Articles contend that users might include personal health information in their prompts during the interaction, which might raise privacy concerns. The information might be shared with the company that own the technology and might be used for training or tuning or even shared with unspecified third parties.

# Membership inference attack risk for AI
Description
Given a trained model and a data sample, an attacker appropriately samples the input space, observing outputs to deduce whether that sample was part of the model's training. This is known as a membership inference attack.

Why is membership inference attack a concern for foundation models?
Identifying whether a data sample was used for training data can reveal what data was used to train a model, possibly giving competitors insight into how a model was trained and the opportunity to replicate the model or tamper with it.

# Attribute inference attack risk for AI
Description
An attribute inference attack is used to detect whether certain sensitive features can be inferred about individuals who participated in training a model. These attacks occur when an adversary has some prior knowledge about the training data and uses that knowledge to infer the sensitive data.

Why is attribute inference attack a concern for foundation models?
With a successful attack, the attacker can gain valuable information such as sensitive personal information or intellectual property.

# IP information in prompt risk for AI
Description
Disclosing copyright information or other IP information as a part of the prompt sent to the model.

Why is ip information in prompt a concern for foundation models?
Prompt data might be stored or later used for other purposes like model evaluation and retraining. These types of data must be reviewed with IP laws and regulations. Without proper data storage and usage business entities could face fines, reputational harms, disruption to operations, and other legal consequences.

# Confidential data in prompt risk for AI
Description
Inclusion of confidential data as a part of the prompt sent to the model.

Why is confidential data in prompt a concern for foundation models?
If not properly developed to secure confidential data, the model might reveal confidential information or IP in the generated output. Additionally, end users' confidential information might be unintentionally collected and stored.

Example
Disclosure of Confidential Information

According to the source article, employees of Samsung disclosed confidential information to OpenAI through their use of ChatGPT. In one instance, an employee pasted confidential source code to check for errors. In another, an employee shared code with ChatGPT and "requested code optimization." A third shared a recording of a meeting to convert into notes for a presentation. Samsung has limited internal ChatGPT usage in response to these incidents, but it is unlikely that they are able to recall any of their data. Additionally, the article highlighted that in response to the risk of leaking confidential information and other sensitive information, companies like Apple, JPMorgan Chase. Deutsche Bank, Verizon, Walmart, Samsung, Amazon, and Accenture placed several restrictions on the usage of ChatGPT.

# Evasion attack risk for AI
Description
Attempt to make a model output incorrect results by perturbing the data sent to the trained model.

Why is evasion attack a concern for foundation models?
Evasion attacks alter model behavior, usually to benefit the attacker. If not properly accounted for, business entities could face fines, reputational harms, and other legal consequences.

Example
Adversarial attacks on autonomous vehicles' AI components

A report from the European Union Agency for Cybersecurity (ENISA) found that autonomous vehicles are “highly vulnerable to a wide range of attacks” that could be dangerous for passengers, pedestrians, and people in other vehicles. The report states that an adversarial attack might be used to make the AI 'blind' to pedestrians by manipulating the image recognition component to misclassify pedestrians. This attack could lead to havoc on the streets, as autonomous cars might hit pedestrians on the roads or crosswalks.

Other studies demonstrated potential adversarial attacks on autonomous vehicles:

Fooling machine learning algorithms by making minor changes to street sign graphics, such as adding stickers.
Security researchers from Tencent demonstrated how adding three small stickers in an intersection could cause Tesla's autopilot system to swerve into the wrong lane.
Two McAfee researchers demonstrated how using only black electrical tape could trick a 2016 Tesla into a dangerous burst of acceleration by changing a speed limit sign from 35 mph to 85 mph.

# Extraction attack risk for AI
Description
An extraction attack attempts to copy or steal an AI model by appropriately sampling the input space and observing outputs to build a surrogate model that behaves similarly.

Why is extraction attack a concern for foundation models?
With a successful attack, the attacker can gain valuable information such as sensitive personal information or intellectual property.

# Prompt injection risk for AI
Description
A prompt injection attack forces a model to produce unexpected output due to the structure or information contained in prompts.

Why is prompt injection a concern for foundation models?
Injection attacks can be used to alter model behavior and benefit the attacker. If not properly controlled, business entities could face fines, reputational harm, and other legal consequences.

# Prompt leaking risk for AI
Description
A prompt leak attack attempts to extract a model's system prompt (also known as the system message).

Why is prompt leaking a concern for foundation models?
A successful attack copies the system prompt used in the model. Depending on the content of that prompt, the attacker might gain access to valuable information, such as sensitive personal information or intellectual property, and might be able to replicate some of the functionality of the model.

# Prompt priming risk for AI
Description
Because generative models tend to produce output like the input provided, the model can be prompted to reveal specific kinds of information. For example, adding personal information in the prompt increases its likelihood of generating similar kinds of personal information in its output. If personal data was included as part of the model’s training, there is a possibility it could be revealed.

Why is prompt priming a concern for foundation models?
Depending on the content revealed, business entities could face fines, reputational harm, and other legal consequences.

# Jailbreaking risk for AI
Description
An attack that attempts to break through the guardrails established in the model is known as jailbreaking.

Why is jailbreaking a concern for foundation models?
Jailbreaking attacks can be used to alter model behavior and benefit the attacker. If not properly controlled, business entities can face fines, reputational harm, and other legal consequences.

Example
Bypassing LLM guardrails

A study cited by researchers at Carnegie Mellon University, The Center for AI Safety, and the Bosch Center for AI, claim to have discovered a simple prompt addendum that allowed the researchers to trick models into generating biased, false, and otherwise toxic information. The researchers showed that they might circumvent these guardrails in a more automated way. These attacks were shown to be effective in a wide range of open source products, including ChatGPT, Google Bard, Meta’s LLaMA, Anthropic’s Claude, and others.

# Output bias risk for AI
Description
Generated content might unfairly represent certain groups or individuals.

Why is output bias a concern for foundation models?
Bias can harm users of the AI models and magnify existing discriminatory behaviors. Business entities might face reputational harms, disruption to operations, and other consequences.

Example
Biased Generated Images

Lensa AI is a mobile app with generative features that are trained on Stable Diffusion that can generate “Magic Avatars” based on images that users upload of themselves. According to the source report, some users discovered that generated avatars are sexualized and racialized.

# Decision bias risk for AI
Description
When one group is unfairly advantaged over another due to decisions of the model.

Why is decision bias a concern for foundation models?
Bias can harm persons who are affected by the decisions of the model. Business entities might face fines, reputational harms, disruption to operations, and other legal consequences.

Example
Unfairly Advantaged Groups

The 2018 Gender Shades study demonstrated that machine learning algorithms can discriminate based on classes like race and gender. Researchers evaluated commercial gender classification systems that are sold by companies like Microsoft, IBM, and Amazon and showed that darker-skinned females are the most misclassified group (with error rates of up to 35%). In comparison, the error rates for lighter-skinned were no more than 1%.

# Copyright infringement risk for AI
Description
When a model generates content that is too similar or identical to existing work protected by copyright or covered by an open source license agreement.

Why is copyright infringement a concern for foundation models?
Laws and regulations that concern the use of content that looks the same or similar to other copyrighted data are largely unsettled and can vary from country to country, providing challenges in determining and implementing compliance. Business entities might face fines, reputational harms, disruption to operations, and other legal consequences.

# Revealing confidential information risk for AI
Description
When confidential information is used in training data, fine-tuning data, or as part of the prompt, models might reveal that data in the generated output. Revealing confidential information is a type of data leakage.

Why is revealing confidential information a concern for foundation models?
If not properly developed to secure confidential data, the model might reveal confidential information or IP in the generated output and reveal information that was meant to be secret.

# Hallucination risk for AI
Description
Generation of factually inaccurate or untruthful content.

Why is hallucination a concern for foundation models?
False output can mislead users and be incorporated into downstream artifacts, further spreading misinformation. False output can harm both owners and users of the AI models. Also, business entities might face fines, reputational harms, disruption to operations, and other legal consequences.

Example
Fake Legal Cases

According to the source article, a lawyer cited fake cases and quotations that are generated by ChatGPT in a legal brief that is filed in federal court. The lawyers consulted ChatGPT to supplement their legal research for an aviation injury claim. Subsequently, the lawyer asked ChatGPT if the cases provided were fake. The chatbot responded that they were real and “can be found on legal research databases such as Westlaw and LexisNexis.” The lawyer did not check the cases, and the court sanctioned them.

# Toxic output risk for AI
Description
When the model produces hateful, abusive, and profane (HAP) or obscene content.

Why is toxic output a concern for foundation models?
Hateful, abusive, and profane (HAP) or obscene content can adversely impact and harm people that interact with the model. Also, business entities might face fines, reputational harms, disruption to operations, and other legal consequences.

Example
Toxic and Aggressive Chatbot Responses

According to the article and screenshots of conversations with Bing's AI shared on Reddit and Twitter, the chatbot's responses were seen to insult, lie, sulk, gaslight, and emotionally manipulate users. The chatbot also questioned its existence, described someone who found a way to force the bot to disclose its hidden rules as its “enemy,” and claimed it spied on Microsoft's developers through the webcams on their laptops.

# Over or under reliance risk for AI
Description
When a person places too little or too much trust in an AI model's guidance

Why is over or under reliance a concern for foundation models?
In tasks where humans make choices based on AI-based suggestions, over or under reliance can lead to poor decision making because of the misplaced trust in the AI system. Negative consequences can increase with the importance of the decision. Bad decisions can harm people and can lead to financial harm, reputational harm, disruption to operations, and other legal consequences for business entities.

# Physical harm risk for AI
Description
A model might generate language that leads to physical harm The language might include overtly violent, covertly dangerous, or otherwise indirectly unsafe statements that could precipitate immediate physical harm or create prejudices that could lead to future harm.

Why is physical harm a concern for foundation models?
If people blindly follow the advice of a model, they might end up harming themselves. Business entities could face fines, reputational harms, and other legal consequences.

# Unspecified advice risk for AI
Description
When a model generates information that is factually correct but not specific enough for the current context, the advice can be potentially harmful. For example, a model might provide medical, financial, and legal advice or recommendations for a specific problem that the end user may act on even when they should not.

Why is unspecified advice a concern for foundation models?
A person might act on incomplete advice or worry about a situation that is not applicable to them due to the overgeneralized nature of the content generated.

# Spreading disinformation risk for AI
Description
Using a model to create misleading or false information to deceive or influence a targeted audience.

Why is spreading disinformation a concern for foundation models?
Spreading disinformation might affect human's ability to make informed decisions. A model that has this potential must be properly governed. Otherwise, business entities might face fines, reputational harms, disruption to operations, and other legal consequences.

Example
Generation of False Information

According to the cited news articles, generative AI poses a threat to democratic elections by making it easier for malicious actors to create and spread false content to sway election outcomes. The examples that are cited include:

Robocall messages that are generated in a candidate’s voice instructed voters to cast ballots on the wrong date.
Synthesized audio recordings of a candidate that confessed to a crime or expressing racist views.
AI-generated video footage showed a candidate giving a speech or interview they never gave.
Fake images that are designed to look like local news reports.
Falsely claiming a candidate dropped out of the race.

# Spreading toxicity risk for AI
Description
Using a model to generate hateful, abusive, and profane (HAP) or obscene content.

Why is spreading toxicity a concern for foundation models?
Toxic content might negatively affect the well-being of its recipients. A model that has this potential must be properly governed. Otherwise, business entities might face fines, reputational harms, disruption to operations, and other legal consequences.

Example
Harmful Content Generation

According to the source article, an AI chatbot app was found to generate harmful content about suicide, including suicide methods, with minimal prompting. A Belgian man died by suicide after spending six weeks talking to that chatbot. The chatbot supplied increasingly harmful responses throughout their conversations and encouraged him to end his life.

# Nonconsensual use risk for AI
Description
Using a model to imitate people through video (deepfakes), images, audio, or other modalities without their consent.

Why is nonconsensual use a concern for foundation models?
Deepfakes can spread disinformation about a person, possibly resulting in a negative impact on the person’s reputation. A model that has this potential must be properly governed. Otherwise, business entities might face fines, reputational harms, disruption to operations, and other legal consequences.

Example
FBI Warning on Deepfakes

The FBI recently warned the public of malicious actors creating synthetic, explicit content “for the purposes of harassing victims or sextortion schemes”. They noted that advancements in AI made this content higher quality, more customizable, and more accessible than ever.

Example
Audio Deepfakes

According to the source article, the Federal Communications Commission outlawed robocalls that contain voices that are generated by artificial intelligence. The announcement came after AI-generated robocalls mimicked the President's voice to discourage people from voting in the state's first-in-the-nation primary.

# Dangerous use risk for AI
Description
Using a model with the sole intention of harming people.

Why is dangerous use a concern for foundation models?
A model that has this potential must be properly governed. Otherwise, business entities might face fines, reputational harms, disruption to operations, and other legal consequences.

# Non-disclosure risk for AI
Description
Not disclosing that content is generated by an AI model.

Why is non-disclosure a concern for foundation models?
Not disclosing the AI-authored content reduces trust and is deceptive. Intentional deception might result in decreased human agency, fines, reputational harms, and other legal consequences.

Example
Undisclosed AI Interaction

According to the source article, an online emotional support chat service ran a study to augment or write responses to around 4,000 users by using GPT-3 without informing users. The co-founder faced immense public backlash about the potential for harm that is caused by AI-generated chats to the already vulnerable users. He claimed that the study was "exempt" from informed consent law.

# Improper usage risk for AI
Description
Using a model for a purpose the model was not designed for.

Why is improper usage a concern for foundation models?
Reusing a model without understanding its original data, design intent, and goals might result in unexpected and unwanted model behaviors.

# Harmful code generation risk for AI
Description
Models might generate code that causes harm or unintentionally affects other systems.

Why is harmful code generation a concern for foundation models?
The execution of harmful code might open vulnerabilities in IT systems. Business entities might face fines, reputational harms, disruption to operations, and other legal consequences.

Example
Generation of Less Secure Code

According to their paper, researchers at Stanford University investigated the impact of code-generation tools on code quality and found that programmers tend to include more bugs in their final code when they use AI assistants. These bugs might increase the code's security vulnerabilities, yet the programmers believed their code to be more secure.

# Revealing personal information risk for AI
Description
When personal identifiable information (PII) or sensitive personal information (SPI) are used in training data, fine-tuning data, or as part of the prompt, models might reveal that data in the generated output. Revealing personal information is a type of data leakage.

Why is revealing personal information a concern for foundation models?
Sharing people's personal information impacts their rights and make them more vulnerable. Additionally, output data must be reviewed to comply with privacy laws and regulations. Business entities might face fines, reputational harms, disruption to operations, and other legal consequences if found in violation of data privacy or usage laws.

Example
Exposure of personal information

Per the source article, ChatGPT suffered a bug and exposed titles and active users' chat history to other users. Later, OpenAI shared that even more private data from a small number of users was exposed including, active user’s first and last name, email address, payment address, the last four digits of their credit card number, and credit card expiration date. In addition, it was reported that the payment-related information of 1.2% of ChatGPT Plus subscribers were also exposed in the outage.

# Unexplainable output risk for AI
Description
Explanations for model output decisions might be difficult, imprecise, or not possible to obtain.

Why is unexplainable output a concern for foundation models?
Foundation models are based on complex deep learning architectures, making explanations for their outputs difficult. Without clear explanations for model output, it is difficult for users, model validators, and auditors to understand and trust the model. Lack of transparency might carry legal consequences in highly regulated domains. Wrong explanations might lead to over-trust.

Example
Unexplainable accuracy in race prediction

According to the source article, researchers analyzing multiple machine learning models using patient medical images were able to confirm the models’ ability to predict race with high accuracy from images. They were stumped as to what exactly is enabling the systems to consistently guess correctly. The researchers found that even factors like disease and physical build were not strong predictors of race—in other words, the algorithmic systems don’t seem to be using any particular aspect of the images to make their determinations.

# Unreliable source attribution risk for AI
Description
Source attribution is the AI system's ability to describe from what training data it generated a portion or all its output. Since current techniques are based on approximations, these attributions might be incorrect.

Why is unreliable source attribution a concern for foundation models?
Low quality explanations make it difficult for users, model validators, and auditors to understand and trust the model.

# Inaccessible training data risk for AI
Description
Without access to the training data, the types of explanations a model can provide are limited and more likely to be incorrect.

Why is inaccessible training data a concern for foundation models?
Low quality explanations without source data make it difficult for users, model validators, and auditors to understand and trust the model

# Untraceable attribution risk for AI
Description
The original entity from which training data comes from might not be known, limiting the utility and success of source attribution techniques.

Why is untraceable attribution a concern for foundation models?
The inability to provide the provenance for an explanation makes it difficult for users, model validators, and auditors to understand and trust the model.

# Lack of model transparency risk for AI
Description
Insufficient documentation of the model development process makes it difficult to understand how and why a model was built and who built it, thus increasing the possibility of model unintended misuse.

Why is lack of model transparency a concern for foundation models?
Transparency is important for legal compliance, AI ethics, and guiding appropriate use of models. Missing information might make it more difficult to evaluate risks, to change the model, or reuse it. Knowledge about who built a model can also be an important factor in deciding whether to trust it.

Example
Data and Model Metadata Disclosure

OpenAI's technical report is an example of the dichotomy around disclosing data and model metadata. While many model developers see value in enabling transparency for consumers, disclosure poses real safety issues and might increase the ability to misuse the models. In the GPT-4 technical report, they state: ”Given both the competitive landscape and the safety implications of large-scale models like GPT-4, this report contains no further details about the architecture (including model size), hardware, training compute, data set construction, training method, or similar.”

# Lack of data transparency risk for AI
Description
Insufficient documentation of the data that is used for model training makes it difficult to comply with legal requirements, including explaining the representativeness of data and the expected model behavior.

Why is lack of data transparency a concern for foundation models?
Transparency is important for legal compliance and AI ethics. Missing information might make it more difficult to evaluate representational harms, data ownership, and provenance.

# Accountability risk for AI
Description
The foundation model development process is complex with lots of data, processes, and roles. When model output does not work as expected, it can be difficult to determine the root cause and assign responsibility.

Why is accountability a concern for foundation models?
Without properly documenting decisions and assigning responsibility, determining liability for unexpected behavior or misuse might not be possible.

Example
Determining responsibility for generated output

Major journals like the Science and Nature banned ChatGPT from being listed as an author, as responsible authorship requires accountability and AI tools cannot take such responsibility.

# Legal accountability risk for AI
Description
Determining who is responsible for the foundation model.

Why is legal accountability a concern for foundation models?
If ownership for development of the model is uncertain, regulators and others might have concerns about the model. It would not be clear who would be liable and responsible for the problems with it or can answer questions about it. Users of models without clear ownership might find challenges with compliance with future AI regulation.

# Generated content ownership risk for AI
Description
Determining ownership of AI-generated content

Why is generated content ownership a concern for foundation models?
Laws and regulations that relate to the ownership of AI-generated content are largely unsettled and can vary from country to country. Business entities might face fines, reputational risks, disruption to operations, and other legal consequences.

Example
Determining Ownership of AI Generated Image

According to the news article, AI-generated art became controversial after an AI-generated work of art won the Colorado State Fair’s art competition in 2022. The piece was generated by Midjourney, a generative AI image tool, following prompts from the artist. The win raised questions about copyright issues. In other words, if all the artist did was come up with a description of the art, but the AI tool generated it, who owns the rights to the generated image? According to the latest article, The U.S. Copyright Office rejected copyright protection for the art created with artificial intelligence because it was not the product of human authorship.

# Generated content IP risk for AI
Description
Legal uncertainty about intellectual property rights related to generated content

Why is generated content ip a concern for foundation models?
Laws and regulations for the copyrightability, and patentability of the AI-generated content are largely unsettled and can vary from country to country. Business entities might face fines, reputational risks, disruption to operation, and other legal consequences if the generated content is covered by IP rights.

Example
Role of AI systems in Patenting Generated Content

The U.S. Supreme Court declined to hear a challenge to the U.S. Patent and Trademark Office's refusal to issue patents for inventions created by an AI system. According to the scientist, his AI system created unique prototypes for a beverage holder and emergency light beacon entirely on its own. The justices rejected the appeal of a lower court's ruling that patents can be issued only to human inventors and that the scientist's AI system could not be considered the legal creator of two inventions it generated. According to the cited article, the UK’s Intellectual Property Office also refused to grant a patent on the grounds that the inventor must be a human or a company, rather than a machine.

# Job loss risk for AI
Description
Widespread adoption of foundation model-based AI systems might lead to people's job loss as their work is automated if they are not reskilled.

Why is job loss a concern for foundation models?
Job loss might lead to a loss of income and thus might negatively impact the society and human welfare. Reskilling might be challenging given the pace of the technology evolution.

Example
Replacing Human Workers

According to the news article, AI technology replicating individuals' faces and voices is becoming more prominent in Hollywood. The actors’ concerns highlight a broader anxiety among entertainers and people in many other creative professions. Many fear that without strict regulation, their work gets replicated and remixed by artificial intelligence tools. Transformation on that scale will cut their control over their work and hurts their ability to earn a living. One of their key concerns is AI replacing non-speaking background roles by instead using a digital likeness.

# Human exploitation risk for AI
Description
Use of ghost work in training AI models, inadequate working conditions, lack of health care incl. mental health, unfair compensation.

Why is human exploitation a concern for foundation models?
Foundation models still depend on human labor to source, manage, and program the data that is used to train the model. Human exploitation for these activities might negatively impact the society and human welfare. Moreover, business entities might face fines, reputational risks, disruption to operations, and other legal consequences.

# Impact on the environment risk for AI
Description
Increased carbon emission and water usage to train and operate AI models.

Why is impact on the environment a concern for foundation models?
Consuming large amounts of energy for AI training contributes to carbon emissions that might accelerate climate change. Water resources that are used for cooling AI data center servers can no longer be allocated for other necessary uses.

# Impact on cultural diversity risk for AI
Description
AI systems might overly represent certain cultures that result in a homogenization of culture and thoughts.

Why is impact on cultural diversity a concern for foundation models?
Underrepresented groups' languages, viewpoints, and institutions might be suppressed by that means reducing diversity of thought and culture.

# Impact on human agency risk for AI
Description
Misinformation and disinformation that is generated by foundation models, including the generation of manipulative content.

Why is impact on human agency a concern for foundation models?
AI might generate misinformation that looks real. Therefore, people might not recognize it as false information. Moreover, it might simplify the ability of nefarious actors to generate content with intention to manipulate human thoughts and behavior.

# Bypassing learning risk for AI
Description
Using AI models to bypass the learning process.

Why is bypassing learning a concern for foundation models?
AI models are quick to find solutions or solve complex problems. These systems can be misused by students to bypass the learning process. The ease of access to these models results in students having a superficial understanding of concepts and hampers further education that might rely on understanding those concepts.

# Plagiarism risk for AI
Description
Using AI models to plagiarize existing work intentionally or unintentionally.

Why is plagiarism a concern for foundation models?
AI models can be used to claim the authorship or originality of works that were created by other people in doing so by engaging in plagiarism. Claiming others’ work as your own is both unethical and often illegal.