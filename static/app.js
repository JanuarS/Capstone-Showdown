$('.edit-user').click(editUser)
$('.delete-user').click(deleteUser)

async function editUser() {
    const id = $(this).data('id')
    await axios.patch(`/user/${id}`)
    alert(`UPDATED ${id}`)
}

async function deleteUser() {
    const id = $(this).data('id')
    await axios.delete(`/user/${id}`)
    alert(`DELETED ${id}`)
}