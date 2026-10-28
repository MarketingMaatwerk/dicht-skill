<?php
/**
 * Sjabloon: opruimen bij het verwijderen van de plugin.
 * Dekt: WP-21, WP-08
 * Aanpassen: de tabel, de opties en de geplande taken van de eigen plugin.
 * Controleren (WP-21): op een schone installatie installeren, gebruiken, verwijderen; daarna tonen
 *   wp db tables en wp option list --search='mmvb_*' niets meer van de plugin.
 * Gevalideerd op 04-10-2026 (PHP 8.3.35, WordPress 7.1.2, MariaDB 10.11, wegwerpcontainer): php -l, en na
 *   wp plugin uninstall zijn de tabel, de optie en de geplande taak weg.
 *
 * @package MM_Voorbeeld
 */

declare(strict_types=1);

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
	exit;
}

global $wpdb;

// phpcs:ignore WordPress.DB.DirectDatabaseQuery, WordPress.DB.DirectDatabaseQuery.SchemaChange -- eigen tabel, bij verwijderen.
$wpdb->query( $wpdb->prepare( 'DROP TABLE IF EXISTS %i', $wpdb->prefix . 'mmvb_items' ) );

delete_option( 'mmvb_instellingen' );
wp_clear_scheduled_hook( 'mmvb_dagelijks' );
