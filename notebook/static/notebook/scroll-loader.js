var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onBeforePageLoad: function () {
        $iml = $("#infinite-more-link")
        if ($iml) window.href = $iml.href
    },
    onAfterPageLoad: function ($items) {
        $(".masonry").masonry('appended', $items);
    }
});