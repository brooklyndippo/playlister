# tests.py
from unittest import TestCase, main as unittest_main, mock
# Add this new import
from bson.objectid import ObjectId
from app import app, video_url_creator

sample_id_list = ['hY7m5jjJ9mM','CQ85sUNBK7w']
# All of these are new mock data that we'll use
sample_playlist_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_playlist = {
    'title': 'Cat Videos',
    'description': 'Cats acting weird',
    'videos': [
        'https://youtube.com/embed/hY7m5jjJ9mM',
        'https://youtube.com/embed/CQ85sUNBK7w'
    ],
    'video_ids': ['hY7m5jjJ9mM','CQ85sUNBK7w']
}
sample_form_data = {
    'title': sample_playlist['title'],
    'description': sample_playlist['description'],
    'videos': '\n'.join(sample_playlist['video_ids'])
}

class PlaylistsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    #TEST INDEX
    def test_index(self):
        """Test the playlists homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')

        page_content = result.get_data(as_text=True)
        self.assertIn('Playlist', page_content)

    #TEST NEW
    def test_new(self):
        """Test the new playlist creation page."""
        result = self.client.get('/playlists/new')
        self.assertEqual(result.status, '200 OK')

        page_content = result.get_data(as_text=True)
        self.assertIn('New Playlist', page_content)

    #TEST VIDEO URL CREATOR
    def test_video_url_creator(self):
        """Test the video_url_creator function"""
        expected_list = ['https://youtube.com/embed/hY7m5jjJ9mM', 'https://youtube.com/embed/CQ85sUNBK7w']
        output_list = video_url_creator(sample_id_list)
        self.assertEqual(expected_list, output_list)

    #TEST SHOW
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_playlist(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = sample_playlist

        result = self.client.get(f'/playlists/{sample_playlist_id}')
        self.assertEqual(result.status, '200 OK')

        page_content = result.get_data(as_text=True)
        self.assertIn('Cat Videos', page_content)

    #TEST EDIT
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_playlist(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = sample_playlist

        result = self.client.get(f'/playlists/{sample_playlist_id}/edit')
        self.assertEqual(result.status, '200 OK')

        page_content = result.get_data(as_text=True)
        self.assertIn('Cat Videos', page_content)

    # TO-DO add tests for create and update function. 
    # Need to debug -- AttributeError: 'NoneType' object has no attribute 'split'
    #TEST CREATE
    #TEST UPDATE


    #TEST DELETE
    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_playlist(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/playlists/{sample_playlist_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_playlist_id})

      
if __name__ == '__main__':
    unittest_main()
