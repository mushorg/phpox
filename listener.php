<?

$host = "localhost";
$port = 1234;
set_time_limit(0);

$socket = socket_create(AF_INET, SOCK_STREAM, 0);
$result = socket_bind($socket, $host, $port);
$result = socket_listen($socket, 3);
$spawn = socket_accept($socket);
$welcome = ":from!server 001\r\n";
socket_write($spawn, $welcome, strlen ($welcome));
$welcome = ":from!server 004 :cmd\r\n";
socket_write($spawn, $welcome, strlen ($welcome));
do
{	
	if (false === ($input = @socket_read($spawn, 1024, 1))) {
            echo "socket_read() failed: reason: " . socket_strerror(socket_last_error($spawn)) . "\n";
            break;
        }
    $input = trim($input);
	if ($input != "")
	{
		$output = $input . "\n";
		socket_write($spawn, $output);
	}
} while (true);
socket_close($socket);
?>
