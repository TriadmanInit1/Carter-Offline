import json
from carterpy import Carter

class CarterOffline:
    def __init__(self, intents_file_path, CarterAPI):
        self.intents_file_path = intents_file_path
        self.intents = self.train()
        self.CarterAPI = CarterAPI

    def tokenize(self, input_string):
        processed_string = input_string.lower().strip().replace(r"[^\w\s]|_", "").replace(r"\s+", " ")
        words = processed_string.split(" ")

        words = self.stem_list(words)

        return words

    def tokenize_list(self, input_list):
        token_words = []
        for word in input_list:
            token = self.tokenize(word)
            token_words.append(token)

        return token_words

    def train(self):
        with open(self.intents_file_path, "r") as file:
            intents = json.load(file)
        return intents

    def pattern_compare(self, input_string):
        input_string_lower = input_string.lower()
        highest_similarity = 0
        most_similar_pattern = None
        similarity_percentage = 0

        for intent_class in self.intents["intents"]:
            overall_word_list = []
            similarity = 0

            for pattern in intent_class["patterns"]:
                word_list = []
                pattern_lower = pattern.lower()
                word_list = self.tokenize(pattern_lower)
                overall_word_list.append(word_list)
                new_list = []
                new_bag = []

                for word in word_list:
                    word = self.stem(word)
                    new_list.append(word)

                word_list_2 = self.tokenize(input_string_lower)
                for word in word_list_2:
                    word = self.stem(word)
                    new_bag.append(word)

                word_list = new_list
                word_list_2 = new_bag

                for word in word_list_2:
                    if word in word_list:
                        similarity += 1

                if similarity > highest_similarity:
                    similarity_percentage = similarity / (len(overall_word_list) + len(word_list_2))
                    highest_similarity = similarity
                    most_similar_pattern = intent_class

        print(f"Similarity: {similarity_percentage:.2%}")

        if most_similar_pattern:
            highest_similarity = highest_similarity / 100
            return most_similar_pattern, highest_similarity
        else:
            raise ValueError("No matching intent class found.")

    def response_compare(self, input_string, intent_class):
        input_string_lower = input_string.lower()
        highest_similarity = 0
        similarity_percentage = 0
        most_similar_response = None

        responses = intent_class["responses"] if intent_class else []

        for response in responses:
            similarity = 0
            response_lower = response.lower()
            word_list = self.tokenize(response_lower)
            new_list = []
            new_bag = []

            for word in word_list:
                word = self.stem(word)
                new_list.append(word)

            word_list_2 = self.tokenize(input_string_lower)
            for word in word_list_2:
                word = self.stem(word)
                new_bag.append(word)

            word_list = new_list
            word_list_2 = new_bag
            overall_word_list = word_list + word_list_2

            for word in word_list_2:
                if word in word_list:
                    similarity += 1

            if similarity > highest_similarity:
                similarity_percentage = similarity / (len(overall_word_list) + len(word_list_2))
                highest_similarity = similarity
                most_similar_response = response

        print(f"Similarity: {similarity_percentage:.2%}")

        # Convert most_similar_response back into the original string
        for response in responses:
            low_response_list = []
            low_response = response.lower()
            low_response_list = self.stem_sentence(low_response)

            for low_response_word in low_response_list:
                if low_response_word == most_similar_response:
                    most_similar_response = response

        return most_similar_response

    def stem(self, input_word):
        suffixes = ["ing", "ly", "ed", "es", "'s", "er", "est", "y", "ily", "able", "ful", "ness", "less", "ment", "ive", "ize", "ous"]
        for suffix in suffixes:
            if input_word.endswith(suffix):
                input_word = input_word[:-len(suffix)]
                break
        return input_word

    def stem_sentence(self, input_string):
        word_list = input_string.split(" ")
        stemmed_words = []
        for input_word in word_list:
            word = self.stem(input_word)
            stemmed_words.append(word)

        return stemmed_words

    def stem_list(self, input_list):
        stemmed_words = []
        for word in input_list:
            stemmed_word = self.stem(word)
            stemmed_words.append(stemmed_word)

        return stemmed_words

    def SendToCarter(self, CarterAPI, input_string, User):
        carter = Carter(CarterAPI)

        ResponseOutput = carter.say(input_string, User)

        intents = self.train()

        target_class = self.pattern_compare(input_string)

        for intent in intents['intents']:
            tag = target_class
            intent_tag = intent.get("tag")
            if intent_tag == tag:
                intent.setdefault("patterns", []).append(input_string)
                intent.setdefault("responses", []).append(ResponseOutput.output_text)

                with open(self.intents_file_path, 'w') as json_file:
                    json.dump(intents, json_file, indent=4, separators=(',', ': '))

        return ResponseOutput.output_text
