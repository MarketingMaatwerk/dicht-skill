<?php
/**
 * Plugin Name:       Dicht Voorbeeld
 * Description:       Sjabloon voor een eigen plugin: nonce, capability, invoer in drie stappen, escapen, $wpdb->prepare, REST met permission_callback.
 * Version:           0.1.0
 * Requires at least: 6.2
 * Requires PHP:      8.2
 * Author:            Marketing Maatwerk
 * License:           GPL-2.0-or-later
 * Text Domain:       dicht-voorbeeld
 *
 * Sjabloon: pluginskelet.
 * Dekt: WP-01, WP-02, WP-05, WP-06, WP-08, WP-09, WP-10, WP-11, WP-13, WP-16, WP-17, WP-18, WP-21, WP-27, API-75,
 *       WEB-29, GIT-105
 * Dekt gedeeltelijk:
 *   - WP-10 vraagt de capability op het object (current_user_can( 'edit_post', $id )). De rijen in dit
 *     voorbeeld zijn geen berichten en hebben geen eigenaar; hier geldt een capability voor de hele lijst
 *     (manage_options). Hangt een rij aan een bericht of gebruiker, controleer dan op dat object.
 *   - WP-12: dit skelet registreert geen wp_ajax_nopriv-actie. Doe dat alleen voor een bewust publieke actie
 *     en zet hem op de lijst.
 *   - WP-37 (PHPCS met de WordPress-regels, Plugin Check, PHPStan als gate) is geen onderdeel van dit bestand.
 * Aanpassen: het voorvoegsel mmvb_ en MMVB_ (WP-21), de tekstdomein, de tabel en de capability.
 *   "Requires at least" is 6.2 vanwege de placeholder %i (WP-16); "Requires PHP" een versie die nog
 *   beveiligingsfixes krijgt (GIT-93, WP-52).
 * Controleren:
 *   php -l op elk bestand; PHPCS, Plugin Check en PHPStan zonder melding (WP-37)
 *   een POST zonder nonce of met de nonce van een ander item geeft 403 (WP-09)
 *   een ingelogde abonnee krijgt 403 op het formulier, het verwijderen en de REST-route (WP-10, WP-13)
 *   installeren, gebruiken, verwijderen: daarna zijn tabel en opties weg (WP-21)
 * Gevalideerd op 04-10-2026 (PHP 8.3.35, WordPress 7.1.2, MariaDB 10.11, wegwerpcontainer): php -l, en gedraaid
 *   via HTTP: zonder nonce, met een foute nonce, met de nonce van een ander item en via GET 403; abonnee 403 op
 *   de pagina, het opslaan, het verwijderen en de REST-route; anoniem 401 op de REST-route; een script in de
 *   titel komt niet in de pagina; een procentteken in de zoekterm werkt niet als jokerteken; geen PHP-melding
 *   in het log. PHPCS, Plugin Check en PHPStan zijn niet gedraaid (WP-37).
 *
 * @package MM_Voorbeeld
 */

declare(strict_types=1);

// Geen directe uitvoering (WP-08).
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const MMVB_CAPABILITY = 'manage_options';
const MMVB_STATUSSEN  = array( 'open', 'dicht' );

/**
 * De naam van de eigen tabel, met het prefix van de site (WP-21).
 */
function mmvb_tabel(): string {
	global $wpdb;
	return $wpdb->prefix . 'mmvb_items';
}

register_activation_hook( __FILE__, 'mmvb_activeren' );

/**
 * Maakt de eigen tabel aan.
 */
function mmvb_activeren(): void {
	global $wpdb;
	require_once ABSPATH . 'wp-admin/includes/upgrade.php';
	$tabel   = mmvb_tabel();
	$charset = $wpdb->get_charset_collate();
	dbDelta(
		"CREATE TABLE {$tabel} (
			id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
			titel varchar(200) NOT NULL,
			status varchar(20) NOT NULL DEFAULT 'open',
			created_at datetime NOT NULL,
			PRIMARY KEY  (id)
		) {$charset};"
	);
}

/**
 * Haalt items op. Elke waarde gaat via prepare met kale placeholders; tabel en kolom via %i (WP-16).
 * De sorteerkolom en de richting komen uit een vaste lijst (WP-18); het zoekpatroon via esc_like (WP-17).
 *
 * @return array<int, object>
 */
function mmvb_items( string $zoek, string $orderby, string $order ): array {
	global $wpdb;
	$kolommen = array(
		'datum' => 'created_at',
		'titel' => 'titel',
	);
	$kolom    = $kolommen[ $orderby ] ?? 'created_at';
	$richting = 'asc' === strtolower( $order ) ? 'ASC' : 'DESC';
	$like     = '%' . $wpdb->esc_like( $zoek ) . '%';

	// phpcs:ignore WordPress.DB.PreparedSQL.InterpolatedNotPrepared -- $richting is hierboven vastgezet op ASC of DESC.
	$sql = $wpdb->prepare( "SELECT id, titel, status, created_at FROM %i WHERE titel LIKE %s ORDER BY %i {$richting} LIMIT %d", mmvb_tabel(), $like, $kolom, 50 );

	// phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared, WordPress.DB.DirectDatabaseQuery -- $sql komt uit prepare; eigen tabel.
	return $wpdb->get_results( $sql );
}

add_action( 'admin_menu', 'mmvb_menu' );

/**
 * Registreert de beheerpagina. De capability hier verbergt alleen het menu; elke handler controleert zelf (WP-11).
 */
function mmvb_menu(): void {
	add_management_page( __( 'Dicht Voorbeeld', 'dicht-voorbeeld' ), __( 'Dicht Voorbeeld', 'dicht-voorbeeld' ), MMVB_CAPABILITY, 'dicht-voorbeeld', 'mmvb_pagina' );
}

/**
 * Toont de lijst en het formulier. Lezen via GET wijzigt niets (WEB-29).
 */
function mmvb_pagina(): void {
	if ( ! current_user_can( MMVB_CAPABILITY ) ) {
		wp_die( esc_html__( 'Geen toegang.', 'dicht-voorbeeld' ), 403 );
	}

	// Invoer in drie stappen: unslash, valideren of opschonen, dan gebruiken (WP-06).
	// phpcs:disable WordPress.Security.NonceVerification.Recommended -- alleen lezen: zoeken en sorteren wijzigen niets.
	$zoek    = isset( $_GET['s'] ) ? sanitize_text_field( wp_unslash( $_GET['s'] ) ) : '';
	$orderby = isset( $_GET['orderby'] ) ? sanitize_key( wp_unslash( $_GET['orderby'] ) ) : 'datum';
	$order   = isset( $_GET['order'] ) ? sanitize_key( wp_unslash( $_GET['order'] ) ) : 'desc';
	// phpcs:enable
	// De kop van wp-admin is hier al verstuurd: wp_die toont de melding en stopt, maar de statuscode blijft 200 (gemeten).
	if ( ! in_array( $orderby, array( 'datum', 'titel' ), true ) || ! in_array( $order, array( 'asc', 'desc' ), true ) ) {
		wp_die( esc_html__( 'Ongeldige invoer.', 'dicht-voorbeeld' ), 400 );
	}

	$items = mmvb_items( $zoek, $orderby, $order );

	// Escape elke uitvoer laat, met de functie van de context (WP-01, WP-02, WP-05).
	echo '<div class="wrap">';
	echo '<h1>' . esc_html__( 'Dicht Voorbeeld', 'dicht-voorbeeld' ) . '</h1>';

	echo '<form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '">';
	echo '<input type="hidden" name="action" value="mmvb_opslaan">';
	wp_nonce_field( 'mmvb_opslaan', 'mmvb_nonce' );
	echo '<label for="mmvb-titel">' . esc_html__( 'Titel', 'dicht-voorbeeld' ) . '</label> ';
	echo '<input type="text" id="mmvb-titel" name="titel" maxlength="200" required> ';
	submit_button( __( 'Toevoegen', 'dicht-voorbeeld' ), 'primary', 'submit', false );
	echo '</form>';

	echo '<table class="widefat striped"><thead><tr>';
	echo '<th>' . esc_html__( 'Titel', 'dicht-voorbeeld' ) . '</th><th>' . esc_html__( 'Status', 'dicht-voorbeeld' ) . '</th><th></th>';
	echo '</tr></thead><tbody>';
	foreach ( $items as $item ) {
		$id = (int) $item->id;
		echo '<tr>';
		echo '<td>' . esc_html( $item->titel ) . '</td>';
		echo '<td>' . esc_html( $item->status ) . '</td>';
		echo '<td><form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '">';
		echo '<input type="hidden" name="action" value="mmvb_verwijderen">';
		echo '<input type="hidden" name="id" value="' . esc_attr( (string) $id ) . '">';
		// De actienaam van de nonce bevat het object (WP-09).
		wp_nonce_field( 'mmvb_verwijderen_' . $id, 'mmvb_nonce' );
		submit_button( __( 'Verwijderen', 'dicht-voorbeeld' ), 'delete small', 'submit', false );
		echo '</form></td>';
		echo '</tr>';
	}
	echo '</tbody></table></div>';
}

add_action( 'admin_post_mmvb_opslaan', 'mmvb_opslaan' );

/**
 * Slaat een item op. Alleen POST (admin_post), eerst de capability, dan de nonce, dan de invoer.
 */
function mmvb_opslaan(): void {
	global $wpdb;
	if ( ! current_user_can( MMVB_CAPABILITY ) ) {
		wp_die( esc_html__( 'Geen toegang.', 'dicht-voorbeeld' ), 403 );
	}
	// Kijk naar de uitkomst van de nonce-controle en stop als hij ontbreekt of onjuist is (WP-09).
	if ( ! isset( $_POST['mmvb_nonce'] ) || ! wp_verify_nonce( sanitize_key( wp_unslash( $_POST['mmvb_nonce'] ) ), 'mmvb_opslaan' ) ) {
		wp_die( esc_html__( 'Verlopen of ongeldige aanvraag.', 'dicht-voorbeeld' ), 403 );
	}

	$titel = isset( $_POST['titel'] ) ? sanitize_text_field( wp_unslash( $_POST['titel'] ) ) : '';
	if ( '' === $titel || mb_strlen( $titel ) > 200 ) {
		wp_die( esc_html__( 'Ongeldige invoer.', 'dicht-voorbeeld' ), 400 );
	}

	// Waar het kan de ingebouwde methoden in plaats van eigen SQL (WP-16).
	// phpcs:ignore WordPress.DB.DirectDatabaseQuery -- eigen tabel.
	$wpdb->insert(
		mmvb_tabel(),
		array(
			'titel'      => $titel,
			'status'     => 'open',
			'created_at' => current_time( 'mysql', true ),
		),
		array( '%s', '%s', '%s' )
	);

	// Doorsturen naar een vast, eigen adres en daarna stoppen (WP-27).
	wp_safe_redirect( admin_url( 'tools.php?page=dicht-voorbeeld' ) );
	exit;
}

add_action( 'admin_post_mmvb_verwijderen', 'mmvb_verwijderen' );

/**
 * Verwijdert een item. De nonce is gebonden aan dit ene item.
 */
function mmvb_verwijderen(): void {
	global $wpdb;
	if ( ! current_user_can( MMVB_CAPABILITY ) ) {
		wp_die( esc_html__( 'Geen toegang.', 'dicht-voorbeeld' ), 403 );
	}
	$id = isset( $_POST['id'] ) ? absint( wp_unslash( $_POST['id'] ) ) : 0;
	if ( $id < 1 ) {
		wp_die( esc_html__( 'Ongeldige invoer.', 'dicht-voorbeeld' ), 400 );
	}
	if ( ! isset( $_POST['mmvb_nonce'] ) || ! wp_verify_nonce( sanitize_key( wp_unslash( $_POST['mmvb_nonce'] ) ), 'mmvb_verwijderen_' . $id ) ) {
		wp_die( esc_html__( 'Verlopen of ongeldige aanvraag.', 'dicht-voorbeeld' ), 403 );
	}

	// phpcs:ignore WordPress.DB.DirectDatabaseQuery -- eigen tabel.
	$wpdb->delete( mmvb_tabel(), array( 'id' => $id ), array( '%d' ) );

	wp_safe_redirect( admin_url( 'tools.php?page=dicht-voorbeeld' ) );
	exit;
}

add_action( 'rest_api_init', 'mmvb_rest' );

/**
 * REST-route met permission_callback en een schema per argument (WP-13).
 */
function mmvb_rest(): void {
	register_rest_route(
		'dicht-voorbeeld/v1',
		'/item/(?P<id>\d+)',
		array(
			'methods'             => WP_REST_Server::EDITABLE,
			'callback'            => 'mmvb_rest_bijwerken',
			'permission_callback' => static function (): bool {
				return current_user_can( MMVB_CAPABILITY );
			},
			'args'                => array(
				'id'     => array(
					'type'              => 'integer',
					'required'          => true,
					'validate_callback' => static function ( $waarde ): bool {
						return is_numeric( $waarde ) && $waarde > 0;
					},
				),
				'status' => array(
					'type'              => 'string',
					'required'          => true,
					'enum'              => MMVB_STATUSSEN,
					'sanitize_callback' => 'sanitize_key',
					'validate_callback' => static function ( $waarde ): bool {
						return in_array( $waarde, MMVB_STATUSSEN, true );
					},
				),
			),
		)
	);
}

/**
 * Werkt de status van een item bij.
 *
 * @return WP_REST_Response|WP_Error
 */
function mmvb_rest_bijwerken( WP_REST_Request $request ) {
	global $wpdb;
	$id     = (int) $request['id'];
	$status = (string) $request['status'];

	// phpcs:ignore WordPress.DB.DirectDatabaseQuery -- eigen tabel.
	$gewijzigd = $wpdb->update( mmvb_tabel(), array( 'status' => $status ), array( 'id' => $id ), array( '%s' ), array( '%d' ) );
	if ( false === $gewijzigd ) {
		// Geen details van de database naar buiten (WEB-62).
		return new WP_Error( 'mmvb_fout', __( 'Er ging iets mis.', 'dicht-voorbeeld' ), array( 'status' => 500 ) );
	}
	if ( 0 === $gewijzigd ) {
		return new WP_Error( 'mmvb_niet_gevonden', __( 'Niet gevonden.', 'dicht-voorbeeld' ), array( 'status' => 404 ) );
	}
	return new WP_REST_Response(
		array(
			'id'     => $id,
			'status' => $status,
		),
		200
	);
}
