var my_profile_opp = document.getElementById('my-profile-opp');
var collections_opp = document.getElementById('collections-opp');


var main_profile = document.getElementById('main-profile');
var main_collections = document.getElementById('main-collections');


my_profile_opp.style.border = '1px solid #000000';
collections_opp.style.border = 'none';

main_profile.style.display = 'inline-block';
main_collections.style.display = 'none';


my_profile_opp.addEventListener('click', function() {
    my_profile_opp.style.border = '1px solid #000000';
    collections_opp.style.border = 'none';

    main_profile.style.display = 'inline-block';
    main_collections.style.display = 'none';
})

collections_opp.addEventListener('click', function() {
    collections_opp.style.border = '1px solid #000000';
    my_profile_opp.style.border = 'none';

    main_collections.style.display = 'inline-block';
    main_profile.style.display = 'none';
})