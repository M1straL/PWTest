const testObject = [{
    'id': "76a268c2-1cc1-4210-9318-0caa60fb5825", 'title': "completed1",
    'completed': true
    },
    {
    'id': "86a268c2-1cc1-4210-2083-0caa60fb5825", 'title': "completed2",
    'completed': true
    },
    {
        'id': "86a268c2-1cc1-4210-1728-0caa60fb5825", 'title': "uncomplited1",
        'completed': false
    },
    {
        'id': "86a268c2-1cc1-4210-4444-0caa60fb5825", 'title': "uncomplited2",
        'completed': false
    }];

// Put the object into storage
localStorage.setItem('react-todos', JSON.stringify(testObject));

// Retrieve the object from storage
const retrievedObject = localStorage.getItem('testObject');

console.log('retrievedObject: ', JSON.parse(retrievedObject));