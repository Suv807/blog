<script type="text/javascript">
alert("jkjkjk");
    function Validate() {
        var password = document.getElementById("loginPassword").value;
        var confirmPassword = document.getElementById("Password").value;
        if (password != confirmPassword) {
            alert("Passwords do not match.");
            return false;
        }
        return true;
    }
</script>