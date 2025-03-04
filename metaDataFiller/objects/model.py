class Model:
    existingModelUrls = []
    newModelUrls = []

    def __init__(self, filename):
        self.fileName = filename
        self.existingModelUrls = []
        self.newModelUrls = []
        self.license = "None"
        self.modelId = "None"
        self.creatorAssigned = False