<?php
header('Content-Type: application/json');

$servername = "localhost";
$username = "web";
$password = "web";
$dbname = "gamedb";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT user_name, time FROM ranking ORDER BY time";
$result = $conn->query($sql);

$data = array();
while($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode($data);

$conn->close();
?>
