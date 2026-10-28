<?php
/**
 * Plugin Name: Dicht Testomgeving afschermen
 * Description: Schermt een test-, staging- of demo-omgeving af: alleen ingelogde gebruikers, en noindex op elke respons.
 * Version:     0.1.0
 * Author:      Marketing Maatwerk
 * License:     GPL-2.0-or-later
 *
 * Sjabloon: mu-plugin voor het afschermen van een testomgeving.
 * Dekt: WEB-72, WP-34, WP-08, WP-61 (anoniem geen REST op de testomgeving), API-75
 * Dekt gedeeltelijk:
 *   - WEB-72 vraagt authenticatie op de webserver (basic auth of een IP-allowlist). Een mu-plugin beschermt
 *     alleen wat door WordPress loopt: bestanden die de webserver zelf uitlevert (wp-content/uploads, statische
 *     bestanden) blijven bereikbaar en krijgen geen X-Robots-Tag. Waar je de webserver kunt instellen heeft
 *     01-nginx/snippets/testomgeving.conf of een .htaccess met basic auth de voorkeur; dit bestand is voor
 *     hosting waar dat niet kan, of als tweede laag.
 *   - "Geen kopie van echte klantdata" (WEB-72, DB-85) regel je in de data.
 * Aanzetten: zet in wp-config.php van de testomgeving
 *     define( 'MM_TESTOMGEVING_AFSCHERMEN', true );
 *   Zonder die regel doet het bestand niets, zodat het op productie geen kwaad kan als het meekomt in een kopie.
 *   Controleer daarom na elke kopie van live naar test dat de regel er staat.
 * Beheer (WP-34): een los bestand in wp-content/mu-plugins, uit de eigen repository, met de versie in de kop.
 *   Vergelijk bij elke controle het bestand op de server met de bron (sha256sum).
 * Controleren (WEB-72):
 *   curl -sI https://<test-host>/                  geeft 302 naar wp-login.php en toont X-Robots-Tag: noindex, nofollow
 *   curl -s -o /dev/null -w '%{http_code}' https://<test-host>/wp-json/wp/v2/posts     geeft 401
 *   een zoekopdracht site:<test-host> geeft geen resultaten
 * Gevalideerd op 04-10-2026 (PHP 8.3.35, WordPress 7.1.2, wegwerpcontainer): php -l, en gedraaid: zonder de
 *   constante gebeurt er niets; met de constante geeft de voorkant 302 naar wp-login.php met X-Robots-Tag, de
 *   REST API anoniem 401, XML-RPC is uit, en een bestand in uploads blijft bereikbaar (de genoemde beperking).
 *   Let op: na het zetten van de constante duurt het enkele seconden (opcache) voor hij geldt.
 *
 * @package MM_Testomgeving
 */

declare(strict_types=1);

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! defined( 'MM_TESTOMGEVING_AFSCHERMEN' ) || true !== MM_TESTOMGEVING_AFSCHERMEN ) {
	return;
}

// Noindex op elke respons die door WordPress loopt, ook de inlogpagina en wp-admin.
add_action(
	'init',
	static function (): void {
		if ( ! headers_sent() ) {
			header( 'X-Robots-Tag: noindex, nofollow' );
		}
	},
	0
);

// De voorkant: alleen voor ingelogde gebruikers. auth_redirect stuurt door naar de inlogpagina en stopt.
add_action(
	'template_redirect',
	static function (): void {
		if ( ! is_user_logged_in() ) {
			auth_redirect();
		}
	},
	0
);

// De REST API: anoniem niets.
add_filter(
	'rest_authentication_errors',
	static function ( $resultaat ) {
		if ( null !== $resultaat ) {
			return $resultaat;
		}
		if ( ! is_user_logged_in() ) {
			return new WP_Error( 'mm_testomgeving', __( 'Inloggen is vereist.', 'default' ), array( 'status' => 401 ) );
		}
		return $resultaat;
	}
);

// XML-RPC uit op de testomgeving.
add_filter( 'xmlrpc_enabled', '__return_false' );
