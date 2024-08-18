# a puppet code that fixes a wordpress site 5xx error to 200 ok
# by editing the mistyped .php to php in the /var/www/html/wp-settings.php file

exec { 'fix-wordpress-server-error':
  command => 'sed -i s/phpp/php/g /var/www/html/wp-settings.php',
  path    => '/usr/bin/:/bin/',
}

