func processImage(a Image) {
    val := detectProductOrFruit(a)

    if val == "product" {
        text := detectTextThroughOCR(a)
        
        // Pass the text to GPT for formatting with metadata and obtaining the number of items
        processedText, itemCount := formatWithMetadataAndItemCount(text)

        // Query the processed text through a vector DB
        isSimilar, productData := queryVectorDB(processedText)

        // Check similarity threshold and metadata (price, netWt) before deciding to add new product or update existing
        if isSimilar && checkMetadata(productData, processedText) {
            // Existing product, log the transaction
            logTransactionToPostgreSQL(productData)
        } else {
            // New product, add to vector DB and log the transaction
            addNewProductToVectorDB(processedText)
            logTransactionToPostgreSQL(processedText)
        }
    } else {
        // If it's a fruit or vegetable
        fruitData, weight := detectFruitAndWeight(a)

        if len(fruitData) > 0 {
            // Process fruit/vegetable data in vector DB and check for similarity
            isSimilar, fruitDBData := queryVectorDB(fruitData)

            if isSimilar && checkMetadata(fruitDBData, fruitData) {
                // Existing fruit/vegetable, log transaction
                logTransactionToPostgreSQL(fruitDBData)
            } else {
                // New fruit/vegetable, add to vector DB and log transaction
                addNewProductToVectorDB(fruitData)
                logTransactionToPostgreSQL(fruitData)
            }

            // Run freshness detection model on the image
            freshnessScore := runFreshnessDetectionModel(a)
            updateFreshnessScore(fruitDBData, freshnessScore)
        }
    }
}
