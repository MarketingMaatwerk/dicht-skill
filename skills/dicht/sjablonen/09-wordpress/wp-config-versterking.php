<?php
/**
 * Sjabloon: regels voor wp-config.php van een klantsite. Geen los bestand om te laden: neem de regels over in
 * wp-config.php, boven de regel "That's all, stop editing".
 *
 * Dekt: WP-38 (alleen de controle), WP-39, WP-40, WP-43, WP-46, WP-47, WP-33
 * Let op: staat een constante al in wp-config.php (WP_DEBUG staat er standaard in), vervang dan die regel; twee keer
 *   define voor dezelfde naam geeft een waarschuwing en de eerste waarde wint.
 * Aanpassen:
 *   - WP_DEBUG_LOG: een pad buiten de webroot, alleen als loggen nodig is (WP-40).
 *   - DISALLOW_FILE_MODS staat er bewust niet in: alleen op sites waar updates aantoonbaar via een andere weg
 *     lopen (WP-39). Anders houdt het de automatische beveiligingsupdates tegen (WP-47, WP-48).
 *   - DISALLOW_UNFILTERED_HTML: alleen op sites waar meer mensen dan de eigenaar beheerder of redacteur zijn en
 *     niemand scripts in berichten hoeft te plakken (WP-46).
 * Sleutels en salts (WP-38): acht unieke, willekeurige waarden per installatie. Kopieer ze nooit uit een sjabloon
 *   of van een andere site; daarom staan ze niet in dit bestand. Vervang ze na elk vermoeden van een lek.
 * Rechten (WP-41): wp-config.php op 400, 440 of 600, geen kopieen met een andere naam in de webroot.
 * Wijzigen op een klantsite is een wijziging van klantdata: alleen na akkoord van Marketing Maatwerk en met een terugweg
 *   (WP-53, INFRA-99).
 * Controleren:
 *   wp config get DISALLOW_FILE_EDIT             toont 1 (WP-39)
 *   wp config get WP_DEBUG                       toont leeg of false, of WP_DEBUG_DISPLAY false en het log buiten de webroot (WP-40)
 *   curl -s -o /dev/null -w '%{http_code}' https://<site>/wp-content/debug.log    geeft 403 of 404 (WP-40)
 *   grep -c "put your unique phrase here" wp-config.php                            geeft 0 (WP-38)
 *   stat -c '%a %U' wp-config.php                                                  toont 400, 440 of 600 (WP-41)
 *   de draaiende kernversie tegen https://api.wordpress.org/core/stable-check/1.0/ (WP-47)
 * Gevalideerd op 04-10-2026 (PHP 8.3.35, WordPress 7.1.2, wegwerpcontainer): php -l, en de regels overgenomen in
 *   een echte wp-config.php: wp config get toont de waarden, wp-admin stuurt door naar https en de beheerder mist
 *   edit_plugins. De waarschuwing over de dubbele WP_DEBUG trad op, zoals hierboven beschreven.
 */

// De bestandseditor in wp-admin uit (WP-39).
define( 'DISALLOW_FILE_EDIT', true );

// Debug uit in productie (WP-40).
define( 'WP_DEBUG', false );
// Als loggen toch nodig is, in plaats van de regel hierboven:
// define( 'WP_DEBUG', true );
// define( 'WP_DEBUG_DISPLAY', false );
// define( 'WP_DEBUG_LOG', '/home/<account>/logs/wp-debug.log' );   // buiten de webroot

// HTTPS voor wp-admin (WP-43). siteurl en home staan op https://.
define( 'FORCE_SSL_ADMIN', true );

// Beveiligingsupdates van de kern automatisch (WP-47). Dit is ook de standaard; nooit op false zetten.
define( 'WP_AUTO_UPDATE_CORE', 'minor' );

// Alleen op sites met meer beheerders of redacteuren (WP-46):
// define( 'DISALLOW_UNFILTERED_HTML', true );

// Sleutels van eigen bouw als constante hier, niet in een optie en niet in een pluginbestand (WP-33):
// define( 'MM_VOORBEELD_API_KEY', '<waarde, nooit in git>' );
