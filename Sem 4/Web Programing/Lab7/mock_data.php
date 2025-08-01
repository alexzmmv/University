<?php

require_once 'includes/db_config.php';

$conn = getDbConnection();

$countries = [
    'France',
    'Italy',
    'Spain',
    'Japan',
    'Greece',
    'Thailand',
    'United States',
    'Australia',
    'Brazil',
    'Morocco'
];

$destinations = [
    [
        'name' => 'Paris',
        'country' => 'France',
        'description' => 'Known as the "City of Light," Paris is famous for its iconic Eiffel Tower, world-class museums, and exquisite cuisine. Stroll along the Seine River, visit the Louvre Museum, and enjoy authentic French pastries at quaint cafes.',
        'tourist_targets' => 'Eiffel Tower, Louvre Museum, Notre-Dame Cathedral, Arc de Triomphe, Montmartre, Champs-Élysées, Palace of Versailles',
        'cost_per_day' => 150.00,
        'security_level' => 1
    ],
    [
        'name' => 'Rome',
        'country' => 'Italy',
        'description' => 'The Eternal City boasts ancient ruins, Renaissance art, and delicious Italian cuisine. Explore historical sites that date back thousands of years and indulge in authentic pasta and gelato.',
        'tourist_targets' => 'Colosseum, Vatican City, Roman Forum, Trevi Fountain, Pantheon, Spanish Steps, Villa Borghese',
        'cost_per_day' => 130.00,
        'security_level' => 2
    ],
    [
        'name' => 'Barcelona',
        'country' => 'Spain',
        'description' => 'A vibrant coastal city known for its unique architecture, lively atmosphere, and beautiful beaches. The works of Antoni Gaudí are scattered throughout the city, giving it a distinctive character.',
        'tourist_targets' => 'Sagrada Familia, Park Güell, Casa Batlló, La Rambla, Gothic Quarter, Barceloneta Beach, Montjuïc',
        'cost_per_day' => 120.00,
        'security_level' => 2
    ],
    [
        'name' => 'Tokyo',
        'country' => 'Japan',
        'description' => 'A fascinating blend of ultra-modern and traditional, Tokyo offers visitors an unforgettable experience with its technological innovations, historic temples, and unique pop culture.',
        'tourist_targets' => 'Tokyo Tower, Senso-ji Temple, Meiji Shrine, Shibuya Crossing, Akihabara, Harajuku, Tsukiji Outer Market',
        'cost_per_day' => 140.00,
        'security_level' => 3
    ],
    [
        'name' => 'Santorini',
        'country' => 'Greece',
        'description' => 'Famous for its stunning white-washed buildings with blue domes overlooking the Aegean Sea. This picturesque island offers breathtaking sunsets, volcanic beaches, and delicious Mediterranean cuisine.',
        'tourist_targets' => 'Oia, Fira, Red Beach, Ancient Thera, Akrotiri Archaeological Site, Santo Wines Winery, Amoudi Bay',
        'cost_per_day' => 160.00,
        'security_level' => 3
    ],
    [
        'name' => 'Bangkok',
        'country' => 'Thailand',
        'description' => 'The capital of Thailand is a bustling metropolis known for its ornate shrines, vibrant street life, and boat-filled canals. The city offers a perfect blend of tradition and modernity.',
        'tourist_targets' => 'Grand Palace, Wat Pho, Wat Arun, Chatuchak Weekend Market, Khaosan Road, Chao Phraya River, Jim Thompson House',
        'cost_per_day' => 70.00,
        'security_level' => 2
    ],
    [
        'name' => 'New York City',
        'country' => 'United States',
        'description' => 'The Big Apple is a global hub of culture, art, fashion, and finance. With its iconic skyline, diverse neighborhoods, and world-class attractions, NYC offers something for everyone.',
        'tourist_targets' => 'Statue of Liberty, Times Square, Central Park, Empire State Building, Brooklyn Bridge, Metropolitan Museum of Art, Broadway',
        'cost_per_day' => 200.00,
        'security_level' => 3
    ],
    [
        'name' => 'Sydney',
        'country' => 'Australia',
        'description' => 'A stunning harbor city known for its iconic Opera House, beautiful beaches, and vibrant culture. Sydney offers visitors a perfect blend of urban excitement and natural beauty.',
        'tourist_targets' => 'Sydney Opera House, Sydney Harbour Bridge, Bondi Beach, Royal Botanic Garden, Darling Harbour, Taronga Zoo, The Rocks',
        'cost_per_day' => 150.00,
        'security_level' => 2
    ],
    [
        'name' => 'Florence',
        'country' => 'Italy',
        'description' => 'The birthplace of the Renaissance, Florence is filled with artistic treasures, architectural masterpieces, and Tuscan cuisine. Walk through historic streets and immerse yourself in Italian culture.',
        'tourist_targets' => 'Uffizi Gallery, Florence Cathedral, Ponte Vecchio, Galleria dell\'Accademia, Pitti Palace, Boboli Gardens, Piazzale Michelangelo',
        'cost_per_day' => 120.00,
        'security_level' => 2
    ],
    [
        'name' => 'Rio de Janeiro',
        'country' => 'Brazil',
        'description' => 'Famous for its stunning beaches, lively carnival, and iconic Christ the Redeemer statue. Rio offers visitors a vibrant atmosphere with breathtaking natural landscapes.',
        'tourist_targets' => 'Christ the Redeemer, Sugarloaf Mountain, Copacabana Beach, Ipanema Beach, Tijuca National Park, Lapa Steps, Maracanã Stadium',
        'cost_per_day' => 90.00,
        'security_level' => 2
    ],
    [
        'name' => 'Kyoto',
        'country' => 'Japan',
        'description' => 'The cultural heart of Japan, Kyoto is home to numerous temples, traditional wooden houses, gardens, and geisha districts. Experience traditional Japanese culture and serene natural beauty.',
        'tourist_targets' => 'Fushimi Inari Shrine, Kinkaku-ji (Golden Pavilion), Arashiyama Bamboo Grove, Kiyomizu-dera Temple, Gion District, Philosopher\'s Path, Nijo Castle',
        'cost_per_day' => 130.00,
        'security_level' => 3
    ],
    [
        'name' => 'Marrakech',
        'country' => 'Morocco',
        'description' => 'A vibrant city known for its maze-like medina, colorful souks, and stunning palaces. Marrakech offers an exotic experience with its rich culture, architecture, and cuisine.',
        'tourist_targets' => 'Jemaa el-Fnaa, Bahia Palace, Koutoubia Mosque, Majorelle Garden, Saadian Tombs, Medina of Marrakech, El Badi Palace',
        'cost_per_day' => 80.00,
        'security_level' => 2
    ]
];

try {
    $conn->exec("DELETE FROM destinations");
    $conn->exec("DELETE FROM countries");
    
    $conn->exec("ALTER TABLE countries AUTO_INCREMENT = 1");
    $conn->exec("ALTER TABLE destinations AUTO_INCREMENT = 1");
    
    echo "<h2>Inserting mock data...</h2>";
    echo "<ul>";
    
    $countryIds = [];
    foreach ($countries as $country) {
        $stmt = $conn->prepare("INSERT INTO countries (name) VALUES (:name)");
        $stmt->bindParam(':name', $country);
        $stmt->execute();
        $countryIds[$country] = $conn->lastInsertId();
        echo "<li>Added country: {$country}</li>";
    }
    
    foreach ($destinations as $destination) {
        $countryId = $countryIds[$destination['country']];
        
        if (!isset($destination['security_level'])) {
            $destination['security_level'] = 1;
        }
        
        $stmt = $conn->prepare("INSERT INTO destinations (name, country_id, description, tourist_targets, cost_per_day, security_level) 
                              VALUES (:name, :country_id, :description, :tourist_targets, :cost_per_day, :security_level)");
        
        $stmt->bindParam(':name', $destination['name']);
        $stmt->bindParam(':country_id', $countryId);
        $stmt->bindParam(':description', $destination['description']);
        $stmt->bindParam(':tourist_targets', $destination['tourist_targets']);
        $stmt->bindParam(':cost_per_day', $destination['cost_per_day']);
        $stmt->bindParam(':security_level', $destination['security_level']);
        
        $stmt->execute();
        echo "<li>Added destination: {$destination['name']} ({$destination['country']})</li>";
    }
    
    echo "</ul>";
    echo "<p><strong>Success!</strong> All mock data has been inserted. <a href='index.php'>Go to homepage</a> to see the destinations.</p>";
    
} catch (PDOException $e) {
    echo "<h2>Error!</h2>";
    echo "<p>Failed to insert mock data: " . $e->getMessage() . "</p>";
}
?>