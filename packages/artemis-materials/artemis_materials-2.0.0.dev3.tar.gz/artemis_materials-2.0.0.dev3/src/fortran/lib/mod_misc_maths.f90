!!!#############################################################################
!!! Code written by Ned Thaddeus Taylor and Francis Huw Davies
!!! Code part of the ARTEMIS group (Hepplestone research group).
!!! Think Hepplestone, think HRG.
!!!#############################################################################
!!! module contains various miscellaneous maths functions and subroutines.
!!! module includes the following functionsand subroutines:
!!! times            (multiplies an array by a scalar value)
!!! gauss            (evaluates a gaussian at a point)
!!! fact             (performs factorial on supplied number)
!!! lnsum            (sum a set of log(i), where i=1,n)
!!! safe_acos        (computes acos safely (rounds to acos(val)=0 when val.ge.1)
!!!##################
!!! overlap_indiv_points (computes overlap between individual points)
!!! overlap              (computes overlap of two functions)
!!! convolve             (computes convolution of two functions)
!!! cross_correl         (computes cross correlation of two functions)
!!!##################
!!! running_avg      (smooths a function using a running average)
!!! mean             (returns the mean of a set of points)
!!! median           (returns the median of a set of points)
!!! mode             (returns the mode of a set of points)
!!! range            (returns the range of a set of points)
!!! normalise        (returns an array normalised to one)
!!! get_turn_points  (returns turning points, assumes input is in order)
!!! get_nth_plane    (returns the two points between which nth plane occurs)
!!!##################
!!! table_func       (computes a custom table function for a single point)
!!! gauss_array      (apply gaussians to a set of points in array)
!!! cauchy_array     (apply cauchy distribution to a set of points in array)
!!! slater_array     (apply slater distribution to a set of points in array)
!!!#############################################################################
module misc_maths
  use artemis__constants, only: real32
  implicit none
  integer, parameter :: QuadInt_K = selected_int_kind (16)




contains

!###############################################################################
  function times(input)
    !! Multiply an array by a scalar value
    implicit none

    ! Arguments
    real(real32), dimension(:),intent(in) :: input
    !! Array to be multiplied

    ! Local variables
    integer :: i
    !! Loop index
    real(real32) :: times
    !! Result of multiplication

    times = 1._real32
    do i = 1, size( input, dim = 1 )
       times=times*input(i)
    end do

  end function times
!###############################################################################


!###############################################################################
  function gauss(pos,centre,sigma,tol) result(output)
    !! Evaluate a Gaussian at a point
    implicit none

    ! Arguments
    real(real32) :: pos
    !! Position to evaluate the Gaussian at
    real(real32) :: centre
    !! Centre of the Gaussian
    real(real32) :: sigma
    !! Width of the Gaussian
    real(real32), intent(in), optional :: tol
    !! Tolerance for the Gaussian

    real(real32) :: output
    !! Output value of the Gaussian

    ! Local variables
    real(real32) :: x
    !! Squared distance from the centre
    real(real32) :: tol_
    !! Tolerance for the Gaussian

    tol_ = 38._real32
    if(present(tol)) tol_ = tol

    x = ( pos - centre ) ** 2._real32 / ( 2._real32 * sigma )
    if( abs(x) .lt. tol_ ) then
       output = exp( -x )
    else
       output = 0._real32
    end if

  end function gauss
!###############################################################################


!!!#####################################################
!!! finds the factorial of n
!!!#####################################################
  integer(kind=QuadInt_K) function fact(n)
    implicit none
    integer :: i,n
    fact=1
    do i=1,n
       fact=fact*i
    end do

    return
  end function fact
!!!#####################################################


!!!#####################################################
!!! Sum of logs of range from 1 to n
!!!#####################################################
  real(real32) function lnsum(n) 
    implicit none
    integer :: i,n
    lnsum=0
    do i=1,n
       lnsum=lnsum+log(real(i))
    end do

    return
  end function lnsum
!!!#####################################################


!!!#####################################################
!!! safe cos
!!!#####################################################
  pure elemental function safe_acos(inval) result(val)
    real(real32), intent(in) :: inval
    real(real32) :: val

    if(abs(inval).ge.1._real32)then
       val=acos(sign(1._real32,inval))
    else
       val=acos(inval)
    end if
   

  end function safe_acos
!!!#####################################################


!!!#############################################################################
!!!#############################################################################
!!!  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
!!!#############################################################################
!!!#############################################################################


!!!#####################################################
!!! find overlap between individual points
!!!#####################################################
  function overlap_indiv_points(f,g) result(overlap)
    implicit none
    integer :: n
    integer :: datsize_f, datsize_g
    real(real32), dimension(:) :: f, g
    real(real32), dimension(:), allocatable :: overlap, y
    
    datsize_f = size(f)
    datsize_g = size(g)

    allocate(y(datsize_f))
    if(allocated(overlap)) deallocate(overlap)
    allocate(overlap(datsize_f))

    do n=1,datsize_f
       y(n) = min(f(n),g(n))
    end do

    overlap = y

    
  end function overlap_indiv_points
!!!#####################################################


!!!#####################################################
!!! find overlap of two functions
!!!#####################################################
  function overlap(f,g)
    implicit none
    integer :: n
    integer :: datsize_f, datsize_g
    real(real32) :: overlap
    real(real32), dimension(:) :: f, g
    real(real32), dimension(:), allocatable :: y
    
    datsize_f = size(f)
    datsize_g = size(g)

    allocate(y(datsize_f))

    do n=1,datsize_f
       y(n) = min(f(n),g(n))
    end do

    overlap = sum(y)

    
  end function overlap
!!!#####################################################


!!!#####################################################
!!! find convolution of two functions
!!!#####################################################
  function convolve(f,g)
    implicit none

    !f is the signal array
    !g is the noise/impulse array
    real(real32), dimension(:), allocatable :: convolve, y
    real(real32), dimension(:) :: f, g
    integer :: datsize_f, datsize_g
    integer :: i,j,k

    datsize_f = size(f)
    datsize_g = size(g)

    allocate(y(datsize_f))
    allocate(convolve(datsize_f))

    !last part
    do i=datsize_g,datsize_f
       y(i) = 0.0
       j=i
       do k=1,datsize_g
          y(i) = y(i) + f(j)*g(k)
          j = j-1
       end do
    end do

    !first part
    do i=1,datsize_g
       y(i) = 0.0
       j=i
       k=1
       do while (j > 0)
          y(i) = y(i) + f(j)*g(k)
          j = j-1
          k = k+1
       end do
    end do

    convolve = y

  end function convolve
!!!#####################################################


!!!#####################################################
!!! find cross-correlation of two functions
!!!#####################################################
  function cross_correl(f,g)
    implicit none

    !f is the signal array
    !g is the noise/impulse array
    real(real32), dimension(:), allocatable :: cross_correl, y
    real(real32), dimension(:) :: f, g
    integer :: datsize_f, datsize_g
    integer :: m,n

    datsize_f = size(f)
    datsize_g = size(g)

    allocate(y(datsize_f))
    allocate(cross_correl(datsize_f))

    nloop: do n=1,datsize_f
       y(n) = 0.0
       mloop: do m=1,datsize_g
          if(m+n.gt.datsize_g) cycle nloop
          y(n) = y(n) + f(m) * g(m + n)
       end do mloop
    end do nloop

    cross_correl = y


  end function cross_correl
!!!#####################################################


!!!#############################################################################
!!!#############################################################################
!!!  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
!!!#############################################################################
!!!#############################################################################


!!!#####################################################
!!! smooths a function using a running average
!!!#####################################################
  function running_avg(in_array,window,lperiodic) result(out_array)
    implicit none
    integer :: i,lw,up,nstep
    integer, intent(in) :: window
    real(real32), dimension(:), intent(in) :: in_array
    real(real32), dimension(size(in_array,dim=1)) :: out_array
    logical, optional :: lperiodic
    
    nstep=size(in_array)
    if(mod(dble(window),2.0).eq.0.0)then
       lw = nint(dble(window)/2.0)-1
       up = nint(dble(window)/2.0)
    else 
       lw = (floor(dble(window)/2.0))
       up = (floor(dble(window)/2.0))
    end if

    out_array=0.0
    if(present(lperiodic))then
       if(lperiodic)then
          do i=1,lw
             out_array(i)=sum(in_array(nstep-lw+i:nstep))+&
                  sum(in_array(1:i+up))
          end do
          do i=lw+1,nstep-up
             out_array(i)=sum(in_array(i-lw:i+up))
          end do
          do i=nstep-up+1,nstep
             out_array(i)=sum(in_array(i-lw:nstep))+&
                  sum(in_array(1:up-(nstep-i)))
          end do
          out_array=out_array/window
          return
       end if
    end if
    out_array=in_array

  end function running_avg
!!!#####################################################


!!!#####################################################
!!! returns the mean of a set of points
!!!#####################################################
  function mean(in_array)
    implicit none
    real(real32) :: mean
    real(real32), dimension(:), intent(in) :: in_array

    mean=sum(in_array)/size(in_array)

  end function mean
!!!#####################################################


!!!#####################################################
!!! returns the median of a set of points
!!!#####################################################
  function median(in_array)
    implicit none
    integer :: i,loc
    real(real32) :: median,oddeven,rtmp1
    real(real32), allocatable, dimension(:) :: cp_array
    real(real32), dimension(:), intent(in) :: in_array

    allocate(cp_array(size(in_array)))
    cp_array=in_array
    do i=1,size(cp_array)
       loc=minloc(cp_array(i:),dim=1)+i-1
       rtmp1=cp_array(i)
       cp_array(i)=cp_array(loc)
       cp_array(loc)=rtmp1
    end do

    oddeven=size(cp_array)/2.0
    if(abs(nint(oddeven)-oddeven).lt.tiny(0.0))then
       median=cp_array(nint(oddeven))
    else
       median=(cp_array(floor(oddeven)) + cp_array(ceiling(oddeven)))/2.0
    end if

  end function median
!!!#####################################################


!!!#####################################################
!!! returns the mode of a set of points
!!!#####################################################
!!! CURRENTLY ONLY FINDS ONE MODE, EVEN IF SET IS BIMODAL OR MULTIMODAL
  function mode(in_array)
    implicit none
    integer :: i,itmp1,maxcount
    real(real32) :: mode
    real(real32), dimension(:), intent(in) :: in_array

    maxcount=0
    do i=1,size(in_array)
       itmp1=count(in_array.eq.in_array(i))
       itmp1=count(abs(in_array-in_array(i)).lt.1.E-8_real32)
       if(itmp1.gt.maxcount)then
          maxcount=itmp1
          mode=in_array(i)
       end if
    end do

  end function mode
!!!#####################################################


!!!#####################################################
!!! returns the range of a set of points
!!!#####################################################
  function range(in_array) result(output)
    implicit none
    real(real32) :: output
    real(real32), dimension(:), intent(in) :: in_array

    output=maxval(in_array)-minval(in_array)

  end function range
!!!#####################################################


!!!#####################################################
!!! returns an array normalised to one
!!!#####################################################
  function normalise(in_array) result(output)
    implicit none
    real(real32) :: sumval
    real(real32), dimension(:), intent(in) :: in_array
    real(real32), dimension(size(in_array)) :: output
    
    sumval=sum(in_array)
    if(sumval.lt.1.E-8_real32)then
       output=in_array
    else
       output=in_array/sum(in_array)
    end if

  end function normalise
!!!#####################################################


!!!#####################################################
!!! finds turning points
!!! ... saves turning points in order of smallest to ...
!!! ... largest
!!!##################################################### 
!!! MAKE IT CHECK THE TURNING POINT IS SUSTAINED ACROSS THE WINDOW
  function get_turn_points(invec,lperiodic,window) result(resvec)
    implicit none
    integer :: i,j,nturn,itmp1,itmp2
    real(real32) :: l_grad,r_grad
    real(real32), dimension(:), intent(in) :: invec
    integer, allocatable, dimension(:) :: tvec1,resvec
    integer, optional :: window
    logical, optional :: lperiodic


    nturn=0
    if(allocated(resvec)) deallocate(resvec)
    allocate(tvec1(size(invec)))
    l_grad=0._real32
    r_grad=invec(2)-invec(1)
    if(present(lperiodic))then
       if(lperiodic)then
          l_grad=invec(1)-invec(size(invec))
          if(sign(1._real32,l_grad).ne.sign(1._real32,r_grad).or.&
               (r_grad.eq.0._real32.and.l_grad.ne.r_grad))then
             nturn=nturn+1
             tvec1(nturn)=1
          end if
       end if
    end if


    do i=2,size(invec)-1
       l_grad=r_grad
       r_grad=invec(i+1)-invec(i)
       if(sign(1._real32,l_grad).ne.sign(1._real32,r_grad).or.&
            (r_grad.eq.0._real32.and.abs(l_grad-r_grad).gt.1.E-5_real32))then
          nturn=nturn+1
          tvec1(nturn)=i
       end if
    end do


    if(present(lperiodic))then
       if(lperiodic)then
          r_grad=invec(1)-invec(size(invec))
          if(sign(1._real32,l_grad).ne.sign(1._real32,r_grad).or.&
               (r_grad.eq.0._real32.and.l_grad.ne.r_grad))then
             nturn=nturn+1
             tvec1(nturn)=size(invec)
          end if
       end if
    end if

    if(present(window))then
       i=1
       reduceloop:do
          if(i.ge.nturn) exit reduceloop
          if(abs(tvec1(i)-tvec1(i+1)).lt.window)then
             itmp1=minloc((/invec(tvec1(i)),invec(tvec1(i+1))/),dim=1)
             tvec1(i+itmp1-1:nturn-1)=tvec1(i+itmp1:nturn)
             nturn=nturn-1
          else
             i=i+1
          end if
       end do reduceloop
    end if


    allocate(resvec(nturn))
    resvec(:nturn)=tvec1(:nturn)
    do i=1,nturn
       itmp1=minloc((/  (invec(resvec(j)),j=i,nturn)  /),dim=1)+i-1
       itmp2=resvec(i)
       resvec(i)=resvec(itmp1)
       resvec(itmp1)=itmp2
    end do

    
  end function get_turn_points
!!!#####################################################


!!!#####################################################
!!! finds location of nth plane in form of the ...
!!! ... start and end coordinates
!!!##################################################### 
  function get_nth_plane(invec,nth,window,is_periodic) result(startend)
    implicit none
    integer :: i,nstep,nplane,udef_window
    real(real32) :: tol
    logical :: is_in_plane
    integer, dimension(2) :: startend
    integer, allocatable, dimension(:,:) :: plane_loc
    real(real32), dimension(:), intent(in) :: invec
    integer, intent(in) :: nth
    integer, optional, intent(in) :: window
    logical, optional, intent(in) :: is_periodic


!!!-----------------------------------------------------------------------------
!!! Defines tolerance of plane height variation and initialises variables
!!!-----------------------------------------------------------------------------
    tol = 0.01_real32*(maxval(invec)-minval(invec))
    if(present(window))then
       udef_window=window
    else
       udef_window=10
    end if

    nplane=0
    nstep = size(invec,dim=1)
    allocate(plane_loc(nstep/udef_window,2))
    plane_loc=0
    is_in_plane=.false.


!!!-----------------------------------------------------------------------------
!!! Loops over points to identify planes
!!!-----------------------------------------------------------------------------
    i=0
    step_loop1: do while(i.le.nstep-udef_window)
       i = i + 1
       if(is_in_plane)then
          if(all(&
               abs(invec(plane_loc(nplane,1):plane_loc(nplane,2))-invec(i)).lt.&
               tol))then
             plane_loc(nplane,2)=i
             cycle step_loop1
          end if
       end if
       
       if(.not.is_in_plane)then
          if(all(abs(invec(i:i+udef_window-1)-invec(i)).lt.tol))then
             is_in_plane=.true.
             nplane = nplane + 1
             plane_loc(nplane,1) = i
             plane_loc(nplane,2) = i + udef_window -1
             i = i + udef_window
          end if
          cycle step_loop1
       end if

       is_in_plane=.false.
       
    end do step_loop1


!!!-----------------------------------------------------------------------------
!!! Handles the last few points depending on whether set is periodic
!!!-----------------------------------------------------------------------------
    if(present(is_periodic))then
       if(plane_loc(nplane,2).eq.nstep-udef_window)then
          step_loop2: do i=nstep-udef_window,nstep
             if(all(&
                  abs(invec(plane_loc(nplane,1):plane_loc(nplane,2))-&
                  invec(i)).lt.tol))then
                plane_loc(nplane,2) = i
             else
                exit step_loop2
             end if
          end do step_loop2
       end if
       if(is_periodic)then
          if(plane_loc(1,1).eq.1.and.&
               plane_loc(nplane,2).eq.nstep)then
             if(all(abs(invec(:plane_loc(1,2))-invec(nstep)).lt.tol))then
                plane_loc(1,1) = plane_loc(nplane,1)
                plane_loc(nplane,:) = 0
                nplane = nplane - 1
             end if
          else
             step_loop3: do i=nstep,nstep-udef_window,-1
                if(all(abs(invec(:plane_loc(1,2))-invec(i)).lt.tol))then
                   plane_loc(1,1)=i
                end if
             end do step_loop3
          end if
       end if

    end if


!!!-----------------------------------------------------------------------------
!!! Sets value of nth plane
!!!-----------------------------------------------------------------------------
    if(nplane.lt.nth)then
       startend=0
    else
       startend=plane_loc(nth,:)
    end if



  end function get_nth_plane
!!!##################################################### 


!!!#############################################################################
!!!#############################################################################
!!!  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
!!!#############################################################################
!!!#############################################################################


!!!#####################################################
!!! Ned's custom table function
!!!#####################################################
!!! BREAKS ON a = 1._real32
!!! ABOVE THIS, res WILL ALWAYS EQUAL 1
!!! a should be between -1 and 1?
  function table_func(x,a) result(res)
    implicit none
    real(real32), intent(in) :: x,a
    real(real32) :: res

    res=( ( cos(x) + a ) + abs( cos(x) - a ) - 2._real32 )/&
         ( 2._real32*a - 2._real32 )


  end function table_func
!!!#####################################################


!!!#####################################################
!!! apply gaussians to a set of points in an array
!!!#####################################################
  function gauss_array(distance,in_array,sigma,tol,norm,mask) &
       result(gauss_func)
    implicit none
    integer :: i,n,init_step
    real(real32) :: x,sigma,tol_,mult
    real(real32), optional :: tol
    logical, optional :: norm
    real(real32), dimension(:), intent(in) :: in_array,distance
    real(real32), dimension(size(distance)) :: gauss_func
    real(real32) :: pi = 4._real32*atan(1._real32)

    logical, dimension(size(distance)), optional, intent(in) :: mask


    tol_ = 38._real32
    if(present(tol)) tol_ = tol
    mult=(1._real32/(sqrt(pi*2._real32)*sigma))
    if(present(norm))then
       if(.not.norm) mult=1._real32
    end if
    
    gauss_func=0._real32
    do n=1,size(in_array)
       if(present(mask))then
          if(.not.mask(n)) cycle
       end if
       init_step=minloc(abs( distance(:) - in_array(n) ),dim=1)
       forward: do i=init_step,size(distance),1
          x=0.5_real32*(( distance(i) - in_array(n) )/sigma)**2._real32
          if(x.gt.tol_) exit forward
          gauss_func(i) = gauss_func(i) + exp(-x) * mult
       end do forward

       backward: do i=init_step-1,1,-1
          x=0.5_real32*(( distance(i) - in_array(n) )/sigma)**2._real32
          if(x.gt.tol_) exit backward
          gauss_func(i) = gauss_func(i) + exp(-x) * mult
       end do backward
    end do



  end function gauss_array
!!!#####################################################


!!!#####################################################
!!! apply cauchy distribution to a set of points in an array
!!!#####################################################
  function cauchy_array(distance,in_array,gamma,tol,norm) result(c_func)
    implicit none
    integer :: i,n,init_step
    real(real32) :: x,gamma,tol_,mult
    real(real32), optional :: tol
    logical, optional :: norm
    real(real32), dimension(:), intent(in) :: in_array,distance
    real(real32), dimension(size(distance)) :: c_func
    real(real32) :: pi = 4._real32*atan(1._real32)


    tol_ = 1.E16_real32
    if(present(tol)) tol_=tol
    mult=(1._real32/(pi*gamma))
    if(present(norm))then
       if(.not.norm) mult=1._real32
    end if
    
    c_func=0._real32
    do n=1,size(in_array)
       init_step=minloc(abs( distance(:) - in_array(n) ),dim=1)
       forward: do i=init_step,size(distance),1
          x = 1._real32 + (( distance(i) - in_array(n) )/gamma)**2._real32
          if(x.gt.tol_) exit forward
          c_func(i) = c_func(i) + 1._real32/(x) * mult
       end do forward

       backward: do i=init_step-1,1,-1
          x = 1._real32 + (( distance(i) - in_array(n) )/gamma)**2._real32
          if(x.gt.tol_) exit backward
          c_func(i) = c_func(i) + 1._real32/x * mult
       end do backward
    end do



  end function cauchy_array
!!!#####################################################


!!!#####################################################
!!! apply slater distribution to a set of points in an array
!!!#####################################################
  function slater_array(distance,in_array,zeta,tol,norm) result(s_func)
    implicit none
    integer :: i,n,init_step
    real(real32) :: x,zeta,tol_,mult
    real(real32), optional :: tol
    logical, optional :: norm
    real(real32), dimension(:), intent(in) :: in_array,distance
    real(real32), dimension(size(distance)) :: s_func
    real(real32) :: pi = 4._real32*atan(1._real32)


    tol_ = 38._real32
    if(present(tol)) tol_=tol
    mult=((zeta**3._real32)/pi)**(0.5_real32)
    if(present(norm))then
       if(.not.norm) mult=1._real32
    end if
    
    s_func=0._real32
    do n=1,size(in_array)
       init_step=minloc(abs( distance(:) - in_array(n) ),dim=1)
       forward: do i=init_step,size(distance),1
          x = zeta*abs( distance(i) - in_array(n) )
          if(x.gt.tol_) exit forward
          s_func(i) = s_func(i) + exp(-x) * mult
       end do forward

       backward: do i=init_step-1,1,-1
          x = zeta*abs( distance(i) - in_array(n) )
          if(x.gt.tol_) exit backward
          s_func(i) = s_func(i) + exp(-x) * mult
       end do backward
    end do


  end function slater_array
!!!#####################################################

end module misc_maths
